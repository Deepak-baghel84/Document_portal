from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException 
from pypdf import PyPDFLoader 
from pathlib import Path 
import sys 
from langchain.text_splitter import CharacterTextSplitter
from datetime import datetime
from utills.model_utils import ModelLoader
from langchain_community.vectorstores import FAISS



class Ingestion:
    def __init__(self, base_dir:Path,faiss_index:str):
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.base_dir = Path(base_dir)
            self.faiss_index = Path(faiss_index)
            self.base_dir.mkdir(parents=True,exist_ok=True)
            self.faiss_index.mkdir(parents=True,exist_ok=True)
            self.model_embedding = ModelLoader().load_embedding()
            
            self.log.info(f"Ingestion initialized with base directory: {self.base_dir} and faiss index: {self.faiss_index}")
        except Exception as e:
            self.log.error(f"Error initializing Ingestion: {e}")
            raise CustomException(e,sys)
        
    def ingest_pdf(self,uploaded_file):   #uploaded_file is a list of pages
        try:
            self.log.info(f"Ingesting {len(uploaded_file)} pdf pages")
            docs = []
            for pages in uploaded_file:
                self.log.info(f"Ingesting {pages}")
                session_file = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                session_file_path = self.base_dir / session_file
                with open(session_file_path,'wb') as f:
                    f.write(pages.read())
                loader = PyPDFLoader(str(session_file_path))
                docs.extend(loader.load())
            self.log.info(f"Ingested {len(docs)} pages")
            self._create_retriever(docs)
        except Exception as e:
            self.log.error(f"Error ingesting pdf pages: {e}")
            raise CustomException(e,sys)
        
    def _create_retriever(self,docs):
        try:
            self.log.info(f"Creating retriever")
            text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)
            self.log.info(f"Created {len(chunks)} chunks")

            vectorstore = FAISS.from_documents(chunks,self.model_embedding)
            vectorstore.save_local(str(self.faiss_index))
            self.log.info(f"Retriever created and saved to {self.faiss_index}")
        except Exception as e:
            self.log.error(f"Error creating retriever: {e}")
            raise CustomException(e,sys)
