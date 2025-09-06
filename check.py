from email.mime import base
from src.doc_chat.doc_retriver import DocumentRetriever
from src.doc_ingestion.data_ingestion import DocumentIngestor

import shutil
from utills.config_util import load_config
import os
from logger.custom_logger import CustomLogger
import datetime
from multiprocessing.managers import BaseManager
from langchain_core.messages import BaseMessage
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from typing import Optional,List
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from utills.model_utils import ModelLoader
from prompt.prompt_analyzer import PROMPT_REGISTRY
from model.base_model import PromptType,SummaryResponse
from pathlib import Path
import sys
from langchain_core.documents import Document
from operator import itemgetter
from dotenv import load_dotenv




##    checking the config by loading it
#def test_load_config():
  #      config = load_config()
   #     llm_block = config["llm"]
    #    provider_ = os.getenv("LLM_PROVIDER", "google")
     #   provider = llm_block.get(provider_, "google")
   #
#
 #       provider_name = provider.get("provider")
  #      model_name = provider.get("model_name")
   #     temperature = provider.get("temperature", 0.2)
    #   print(f"Provider: {provider_name}, Model: {model_name}, Temperature: {temperature}, Max Tokens: {max_tokens}")
#
#test_load_config()


#def test_log(log_dir='log'):
        
#    Initialize the custom logger.
#    :param log_dir: Directory where log files will be stored.
        
        #log_file = os.path.join(os.getcwd(), log_dir)
        ##os.makedirs(log_file, exist_ok=True)
        #print(log_file)
        
        # Create a log file with the current date and time
       # log_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
       # print(log_file_name)
       # log_file_path = os.path.join(log_file, log_file_name)
       # print(log_file_path)
    

#test_log()
#def test_file_existence():
#      file_paths = ["Data//Resume.pdf","Data//Sample.pdf","Data//Deepak_Baghel_Resume.pdf"]
      
#      from pathlib import Path
#      uploaded_files = []
#      for file_path in file_paths:
#          if Path(file_path).exists():
#              uploaded_files.append(open(file_path, "rb"))
#          else:
#              print(f"File does not exist: {file_path}")
              

#      for file in uploaded_files:         # file= <_io.BufferedReader name='Data//Resume.pdf'>
       # print(Path(file.name))
#        file_name = os.path.basename(file.name)    
#        print(Path(file_name).suffix)
       # print(file.read(100))
                                              
#test_file_existence()

       # checking session and log deletion 

base_dir = Path("Data/comparator_archive")
def remove_pdf_files(base_dir,keep_latest:int=3):
        """Remove the PDF files from the session directory."""
        try:
            sessions = sorted([f for f in base_dir.iterdir() if f.is_dir()], reverse=True)
            print(sessions)
            if len(sessions) > keep_latest:
                del_session = sessions[0]
                shutil.rmtree(del_session, ignore_errors=True)
                log.info(f"Old session removed successfully name: {sessions[-1]}")
           # for pdf_file in self.session_path.glob("*.pdf"):
           
                    #pdf_file.unlink()
          #  self.session_path.rmdir()  # Remove the session directory if empty
            log.info(f"Old PDF file and session removed successfully name: {del_session}")
                
        except Exception as e:
            log.error(f"Error removing PDF files: {e}")
            raise CustomException(f"Error removing PDF files: {e}", sys)
        


remove_pdf_files(base_dir,keep_latest=3)




