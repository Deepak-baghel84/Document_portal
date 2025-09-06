from numpy import save
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException 
from langchain_community.document_loaders import PyPDFLoader,TextLoader, Docx2txtLoader
from pathlib import Path 
import sys 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
from utills.model_utils import ModelLoader
from langchain_community.vectorstores import FAISS
from datetime import datetime,timezone
import uuid
import os
import shutil
from pypdf import PdfReader



accepted_file_format = {".pdf",".txt",".md",".docs"}

class DocumentIngestor:
    
    def __init__(self,file_path:str="Data//multidoc_archive",session_id:str=None,faiss_index_path:str="Data//faiss_index"):
        """
        Initializes the DocumentIngestor with paths for file storage and FAISS index.
        :param file_path: Directory where documents will be stored.
        :param session_id: Unique identifier for the session, defaults to current timestamp.
        :param faiss_index_path: Directory where FAISS index will be stored.
        """
        
        try:
            self.file_path = Path(file_path)
            self.faiss_index_path = Path(faiss_index_path)
            self.file_path.mkdir(parents=True,exist_ok =True)
            self.faiss_index_path.mkdir(parents=True,exist_ok=True)

            self.session_id_ = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_id = Path(self.session_id_)
            self.temp_path = self.file_path / self.session_id
            self.session_faiss_index = self.faiss_index_path / self.session_id
            self.temp_path.mkdir(parents=True,exist_ok=True)
            self.session_faiss_index.mkdir(parents=True,exist_ok=True)

            self.model = ModelLoader()
            self.embed = self.model.load_embedding()
            
            log.info("DocumentIngestor successfully initialized")
            
          

        except Exception as e:
            log.error("error in initialization DocumentIngestor")
            raise (e,sys)
        
    def ingest_file(self,uploaded_files,session_id=None):
        try:
            documents = []
            for file in uploaded_files:
                file_name = os.path.basename(file.name)
                if Path(file_name).suffix.lower() not in {".pdf", ".txt", ".docs"}:
                    log.error(f"Unsupported file format: {Path(file_name).suffix}")
                    continue
                new_file_path = self.temp_path / file_name    # problem in file name
                with open(new_file_path, 'wb') as f:
                    f.write(file.read())

                if Path(file_name).suffix.lower() == ".pdf":
                    loader = PyPDFLoader(str(new_file_path))
                elif Path(file_name).suffix.lower() == ".txt":
                    loader = TextLoader(str(new_file_path), encoding="utf-8")
                elif Path(file_name).suffix.lower() == ".docs":
                    loader = Docx2txtLoader(str(new_file_path))
                else:
                    log.warning(f"Unsupported file format: {file.suffix}")
                    continue
                docs = loader.load()
                documents.extend(docs)
                #log.info(f"Loaded {len(docs)} pages from {file_name}")

            if documents == []:
                log.error("No valid documents were loaded.")
                raise CustomException("No valid documents were loaded.", sys)
            
            log.info(f"Files saved successfully at {self.temp_path} and loaded into documents list")
            return documents
        except Exception as e:
            log.error(f"Error during file ingestion: {e}")
            raise CustomException(f"Error during file ingestion: {e}", sys)
        
    def create_retrivel(self,documents):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = text_splitter.split_documents(documents)
            log.info(f"Documents splited into {len(split_docs)} chunks")
            self.vectorstore = FAISS.from_documents(split_docs, self.embed)
            self.vectorstore.save_local(self.session_faiss_index)
            log.info(f"FAISS index built and saved at {self.session_faiss_index}")

            retriver = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            return retriver
        except Exception as e:
            log.error(f"Error in creating retrivel: {e}")
            raise CustomException(f"Error building retriver: {e}", sys)
        


class AnalyzeIngestor():
    def __init__(self,dir_path:str="Data//analyzer_archive",session_id:str=None):
        """Initialize the DataIngestion class with file path and session ID.
        :param file_path: Path to the PDF file to be processed.
        :param session_id: Unique identifier for the session.  
        """
        try:
          self.dir_path = dir_path or os.getenv("DEFAULT_FILE_PATH",os.path.join(os.getcwd(), "data","archive_pdfs"))
          self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

          self.new_dir_path = os.path.join(self.dir_path,self.session_id)
          self.new_file = os.makedirs(self.new_dir_path, exist_ok=True)
          log.info(f"Directory created at: {self.new_dir_path}")
        except:
            log.error(f"Error initializing DataIngestion with file path: {dir_path} and session ID: {session_id}")
            raise CustomException("Failed to initialize DataIngestion", sys)
                                  
    def save_pdf(self,uploaded_files):
        try:
            file_name = os.path.basename(uploaded_files.name)
            if Path(file_name).suffix.lower() not in accepted_file_format:
                log.error(f"Unsupported file format: {Path(file_name).suffix}")
                raise CustomException(f"Unsupported file format: {Path(file_name).suffix}", sys)
            
            self.save_path = os.path.join(self.new_dir_path,file_name)
            with open(self.save_path, 'wb') as file:
                file.write(uploaded_files.getbuffer())

            log.info(f"PDF saved successfully at: {self.save_path}")

        except FileNotFoundError as e:
            log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)

    def read_pdf(self):
        documents = []
        try:
            with open (self.save_path, 'rb') as file:
                if Path(self.save_path).suffix.lower() == ".pdf":
                    loader = PyPDFLoader(self.save_path)
                elif Path(self.save_path).suffix.lower() == ".txt":
                    loader = TextLoader(self.save_path, encoding="utf-8")
                elif Path(self.save_path).suffix.lower() == ".docs":
                    loader = Docx2txtLoader(self.save_path)
                else:
                    log.warning(f"Unsupported file format: {Path(self.save_path).suffix}")
                    raise CustomException(f"Unsupported file format: {Path(self.save_path).suffix}", sys)
                
                docs = loader.load()
                documents.extend(docs)
                #log.info(f"Loaded {len(docs)} pages from {file_name}")

            if documents == []:
                log.error("No valid documents were loaded.")
                raise CustomException("No valid documents were loaded.", sys)
            
            log.info(f"Files loaded into documents list successfully from {self.save_path}")
            return documents
        except Exception as e:
            log.error(f"Error during extracting file: {e}")
            raise CustomException(f"Error during extraction of documents: {e}", sys)


class CompareIngestor():
    def __init__(self, dir_path: str = "Data//comparator_archive", session_id: str = None):
        """
        Initialize the DataIngestion class with file path and session ID.
        :param file_path: Path to the PDF file to be processed.
        :param session_id: Unique identifier for the session.  
        """
        try:
            # Set base directory for saving PDFs
            self.base_dir = dir_path or os.getenv("DEFAULT_FILE_PATH", os.path.join(os.getcwd(), "data", "archive_pdfs"))
            
            self.sessionn_file = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_path = Path(self.base_dir) / Path(self.sessionn_file)
            self.session_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            log.error(f"Error initializing Ingestor: {e}")
            raise CustomException(e, sys)
    def save_pdf_files(self,ref_file,act_file):
        """Save the PDF files to the specified directory.
        :param ref_file: Path to the reference PDF file.
        :param act_file: Path to the actual PDF file.
        :return: Paths where the PDF files are saved.
        """
        try:
            self.ref_file = ref_file
            self.act_file = act_file
            #if not self.ref_file.name.lower().endswith('.pdf') or not self.act_file.name.lower().endswith('.pdf'):
             #   raise ValueError("One or both files are not PDFs.")
            ref_save_path = self.session_path / Path(self.ref_file.name)
            act_save_path = self.session_path / Path(self.act_file.name)
            with open(ref_save_path, 'wb') as file:
                file.write(self.ref_file.get_buffer())
            with open(act_save_path, 'wb') as file:
                file.write(self.act_file.get_buffer())
            log.info(f"PDF files saved successfully at: {self.session_path}")

            self._remove_pdf_files(keep_latest=3)
            #return ref_save_path, act_save_path

        except FileNotFoundError as e:
            log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)

    def read_pdf(self, file_path:Path):
        """Read the PDF file and return its content.
        :param file_path: Path to the PDF file to be read.
        :return: Text content of the PDF file.
        """
        try:
            data_block = []
            number = 1
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text.strip():
                        data_block.append(f"file-Page ---{number}---: \n{text}")
                    number += 1
                       
            if not data_block:
                raise ValueError("No text found in the PDF file.")
            
            log.info(f"PDF read successfully from: {file_path}")
            if data_block == []:
                raise ValueError("PDF file is empty or could not be read.")
            return "\n".join(data_block)
        except FileNotFoundError as e:
            log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)
        

    def combine_pdf_text(self):
        """Combine the text from the reference and actual PDF files.
        :param ref_text: Text content of the reference PDF file.
        :param act_text: Text content of the actual PDF file.
        :return: Combined text content.
        """
        try:
            documents = []
            for pdf_file in sorted(self.session_path.iterdir()):
                if pdf_file.suffix.lower() == '.pdf':
                    content = self.read_pdf(pdf_file)
                documents.append(content)
            combined_text = "".join(documents)
            if not combined_text:
                raise ValueError("No text found in the PDF files.")
            log.info("PDF text combined successfully.")
            return combined_text
        except Exception as e:
            log.error(f"Error combining PDF text: {e}")

            raise CustomException(e, sys)
        


    def _remove_pdf_files(self,keep_latest:int=3):
        """Remove the PDF files from the session directory."""
        try:
            sessions = sorted([f for f in self.base_dir.iterdir() if f.is_dir()], reverse=True)
            print(sessions)
            if len(sessions) > keep_latest:
                shutil.rmtree(sessions[-1], ignore_errors=True)
                log.info(f"Old session removed successfully name: {sessions[-1]}")
           # for pdf_file in self.session_path.glob("*.pdf"):
           
                    #pdf_file.unlink()
          #  self.session_path.rmdir()  # Remove the session directory if empty
            log.info(f"Old PDF file and session removed successfully name: {self.session_path}")
                
        except Exception as e:
            log.error(f"Error removing PDF files: {e}")
            raise CustomException(f"Error removing PDF files: {e}", sys)