from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException 
from pypdf import PyPDFLoader 
from pathlib import Path 
import sys 
from langchain.text_splitter import CharacterTextSplitter
from datetime import datetime
from utills.model_utils import ModelLoader
from langchain_community.vectorstores import FAISS
from datetime import datetime,timezone
import uuid
from langchain.document_loaders import TextLoader, Docx2txtLoader




class DocumentIngestor:
    def __init__(self,file_path:str="Data//multidoc_archive",session_id:str=None,faiss_index_path:str=None):
        """
        Initializes the DocumentIngestor with paths for file storage and FAISS index.
        :param file_path: Directory where documents will be stored.
        :param session_id: Unique identifier for the session, defaults to current timestamp.
        :param faiss_index_path: Directory where FAISS index will be stored.
        """
        accepted_file_format = {".pdf",".txt",".md",".docs"}
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.file_path = Path(file_path)
            self.faiss_index_path = Path(faiss_index_path)
            self.file_path.mkdir(parents=True,exist_ok =True)
            self.faiss_index_path.mkdir(parents=True,exist_ok=True)

            self.session_id = session_id or str(datetime.now(timezone.utc).timestamp())
            self.temp_path = self.file_path / Path(self.session_id)
            self.session_faiss_index = self.faiss_index_path / Path(self.session_id)
            self.session_id.mkdir(parents=True,exist_ok=True)
            self.session_faiss_index.mkdir(parents=True,exist_ok=True)

            self.model = ModelLoader()
            
            self.log.info("DocumentIngestor successfully initialized")
          

        except Exception as e:
            self.log.error("error in initialization DocumentIngestor")
            raise (e,sys)
        
    def ingest_file(self,uploaded_files,session_id=None):
        try:
            documents = []
            for file in uploaded_files:
                if file.suffix.lower() not in {".pdf",".txt",".md",".docs"}:
                    self.log.error(f"Unsupported file format: {file.suffix}")
                    continue
                new_file_path = self.temp_path / Path(file.name)
                with open(new_file_path, 'wb') as f:
                    f.write(file.read())

                if file.suffix.lower() == ".pdf":
                    loader = PyPDFLoader(str(new_file_path))
                elif file.suffix.lower() == ".txt":
                    loader = TextLoader(str(new_file_path), encoding="utf-8")
                elif file.suffix.lower() == ".docs":
                    loader = Docx2txtLoader(str(new_file_path))
                else:
                    self.log.warning(f"Unsupported file format: {file.suffix}")
                    continue
                docs = loader.load()
                docs.extend(documents)


            self.log.info(f"Files saved successfully at {self.temp_path} and loaded into documents list")
            return documents
        except Exception as e:
            self.log.error(f"Error during file ingestion: {e}")
            raise CustomException(f"Error during file ingestion: {e}", sys)
        
    def create_retrivel(self,documents):
        try:
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = text_splitter.split_documents(documents)
            self.log.info(f"Documents splited into {len(split_docs)} chunks")

            self.embedding = self.model.load_embeddings()
            self.vectorstore = FAISS.from_documents(split_docs, self.embedding)
            self.vectorstore.save_local(self.session_faiss_index)
            self.log.info(f"FAISS index built and saved at {self.session_faiss_index}")

            retriver = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            return retriver
        except Exception as e:
            self.log.error(f"Error building LCEL chain: {e}")
            raise CustomException(f"Error building LCEL chain: {e}", sys)
        


