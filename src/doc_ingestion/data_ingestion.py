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





class DocumentIngestor:
    #accepted_file_format = {".pdf",".txt",".md",".docs"}
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
                log.info(f"Loaded {len(docs)} pages from {file_name}")

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
            self.vectorstore = FAISS.from_documents(split_docs, self.embedding)
            self.vectorstore.save_local(self.session_faiss_index)
            log.info(f"FAISS index built and saved at {self.session_faiss_index}")

            retriver = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            return retriver
        except Exception as e:
            log.error(f"Error in creating retrivel: {e}")
            raise CustomException(f"Error building retriver: {e}", sys)
        


