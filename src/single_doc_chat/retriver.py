from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from utills.model_utils import ModelLoader
from pathlib import Path
import sys
from langchain_core.documents import Document





class Retriver:
    def __init__(self,faiss_index:Path,user_query:str):
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.faiss_index_path = Path(faiss_index)
            self.user_query = user_query
            self.embeddings = ModelLoader().load_embedding()
            self.faiss_index = FAISS.load_local(self.faiss_index_path,self.embeddings,allow_dangerous_deserialization=True)
            self.retriver = self.faiss_index.as_retriever(search_type="similarity",search_kwargs={"k":5})
            self.log.info(f"Retriver initialized with faiss index: {self.faiss_index} and user query: {self.user_query}")
        except Exception as e:
            self.log.error(f"Error initializing Retriver: {e}")
            raise CustomException(e,sys)
        
    def get_relevant_docs(self):
        try:
            self.log.info(f"Getting relevant docs for user query: {self.user_query}")
            docs = self.retriver.get_relevant_documents(self.user_query)
            self.log.info(f"Found {len(docs)} relevant docs")
            return docs
        except Exception as e:
            self.log.error(f"Error getting relevant docs: {e}")
            raise CustomException(e,sys)

