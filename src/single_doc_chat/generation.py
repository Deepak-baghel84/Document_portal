from langchain_core.output_parsers import StrOutputParser
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from utills.model_utils import ModelLoader
from dotenv import load_dotenv
from model.base_model import PromptType,SummaryResponse
from prompt.prompt_analyzer import Prompt_directory
from pathlib import Path
import sys




class Generation:
    def __init__(self,faiss_index:Path,user_query:str):
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.faiss_index_path = Path(faiss_index)
            self.user_query = user_query
            self.embeddings = ModelLoader().load_embedding()
            self.faiss_index = FAISS.load_local(self.faiss_index_path,self.embeddings,allow_dangerous_deserialization=True)
            self.retriver = self.faiss_index.as_retriever(search_type="similarity",search_kwargs={"k":5})

        except:
            pass
