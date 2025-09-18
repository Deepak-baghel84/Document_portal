from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException 
from langchain_community.document_loaders import PyPDFLoader,TextLoader, Docx2txtLoader
from pathlib import Path 
import sys 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
from utils.model_utils import ModelLoader
from utils.document_ops import load_documents
from langchain_community.vectorstores import FAISS
from datetime import datetime
import uuid
import os
from typing import List, Optional, Iterable
from pypdf import PdfReader



class ChatIngestor():
    """Class to handle document ingestion and FAISS index creation for chat applications.
    """
    
    def __init__(self,temp_base: str = "data",faiss_base: str = "faiss_index",use_session_dirs: bool = True,session_id: Optional[str] = None,):
        """
        Initializes the DocumentIngestor with paths for file storage and FAISS index.
        :param file_path: Directory where documents will be stored.
        :param session_id: Unique identifier for the session, defaults to current timestamp.
        :param faiss_index_path: Directory where FAISS index will be stored.
        """
        
        try:
            self.model_loader = ModelLoader()
            
            self.use_session = use_session_dirs
            self.session_id = session_id or generate_session_id()
            
            self.temp_base = Path(temp_base); self.temp_base.mkdir(parents=True, exist_ok=True)
            self.faiss_base = Path(faiss_base); self.faiss_base.mkdir(parents=True, exist_ok=True)
            
            self.temp_dir = self._resolve_dir(self.temp_base)
            self.faiss_dir = self._resolve_dir(self.faiss_base)

            log.info("ChatIngestor initialized",
                      session_id=self.session_id,
                      temp_dir=str(self.temp_dir),
                      faiss_dir=str(self.faiss_dir),
                      sessionized=self.use_session)
        except Exception as e:
            log.error("Failed to initialize ChatIngestor", error=str(e))
            raise Exception("Initialization error in ChatIngestor", e) from e
            
          

        except Exception as e:
            log.error("error in initialization DocumentIngestor")
            raise (e,sys)
        
    def ingest_file(self,uploaded_files,session_id=None):
        try:
            if not uploaded_files or len(uploaded_files) == 0:
                log.error("No files provided for ingestion.")
                raise CustomException("No files provided for ingestion.", sys)
            for file in uploaded_files:
                log.info(f"Loading document from path: {file}")
                file_name = os.path.basename(file.name)
                new_file_path = self.temp_path / file_name    
                with open(new_file_path, 'wb') as f:
                    f.write(file.read())

            documents = load_documents(uploaded_files)

            if documents == []:
                log.error("No valid documents were loaded.")
                raise CustomException("No valid documents were loaded.", sys)
            
            log.info(f"Files saved successfully at {self.temp_path} and loaded into documents list")

            _remove_pdf_files(base_dir=self.file_path)
            return documents
        except Exception as e:
            log.error(f"Error during file ingestion: {e}")
            raise CustomException(f"Error during file ingestion: {e}", sys)
        
    def create_retrivel(self,documents: Iterable,*,chunk_size: int = 1000,chunk_overlap: int = 200,k: int = 5):
        try:
            paths = save_uploaded_files(documents, self.temp_dir)
            docs = load_documents(paths)
            if not docs:
                raise ValueError("No valid documents loaded")
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
        


class DocHandler():
    def __init__(self,dir_path:Optional[str]="Data//analyzer_archive",session_id:Optional[str]=None):
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
            save_path = os.path.join(self.new_dir_path,file_name)
            with open(save_path, 'wb') as file:
                file.write(open(uploaded_files, "rb").read())

            log.info(f"PDF saved successfully at: {save_path}")
            _remove_pdf_files(base_dir=self.dir_path)
            return save_path
        except FileNotFoundError as e:
            log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)

    def read_pdf(self,file_path:Path):
        
        try:
            text_chunks = []
            number = 1
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text.strip():
                        text_chunks.append(f"file-Page ---{number}---: \n{text}")
                    number += 1  # type: ignore
            text = "\n".join(text_chunks)
            log.info("PDF read successfully", pdf_path=file_path, session_id=self.session_id, pages=len(text_chunks))
            return text
        except Exception as e:
            log.error("Failed to read PDF", error=str(e), pdf_path=file_path, session_id=self.session_id)
            raise Exception(f"Could not process PDF: {file_path}", e) from e


class DocumentComparator():
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
                file.write(open(ref_file, "rb").read())
            with open(act_save_path, 'wb') as file:
                file.write(open(act_file, "rb").read())
            log.info(f"PDF files saved successfully at: {self.session_path}")

            _remove_pdf_files(base_dir=self.base_dir)

            return ref_save_path, act_save_path

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
            doc_parts = []
            for file in sorted(self.session_path.iterdir()):
                if file.is_file() and file.suffix.lower() == ".pdf":
                    content = self.read_pdf(file)
                    doc_parts.append(f"Document: {file.name}\n{content}")
            combined_text = "\n\n".join(doc_parts)
            log.info("Documents combined", count=len(doc_parts), session=self.session_id)
            return combined_text
        except Exception as e:
            log.error("Error combining documents", error=str(e), session=self.session_id)
            raise Exception("Error combining documents", e) from e

def _remove_pdf_files(base_dir="Data/archive",log_dir="logs",keep_latest:int=3):
        """Remove the PDF files from the session directory."""
        try:
            _base_dir = Path(base_dir)
            _log_dir = Path(log_dir)
            sessions = sorted([f for f in _base_dir.iterdir() if f.is_dir()], reverse=True)
            print(sessions)
            if len(sessions) > keep_latest:
                for session in sessions[keep_latest:]:
                    if os.path.exists(log_file):
                      os.remove(session)
                log.info(f"Old session removed successfully ")
              
            
            logs = sorted([f for f in _log_dir.iterdir() if f.is_file() and f.suffix == '.log'], reverse=True)
            if len(logs) > keep_latest:
                for log_file in logs[keep_latest:]:
                    if os.path.exists(log_file):
                      os.remove(log_file)
                log.info(f"Old logs removed successfully ")

            return
        except Exception as e:
            log.error(f"Error removing files or logs: {e}")
            raise CustomException(f"Error removing files or logs: {e}", sys)