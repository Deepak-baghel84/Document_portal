import os
import sys
from turtle import mode
from dotenv import load_dotenv

from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from utils.config_util import load_config

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from logger import GLOBAL_LOGGER as log







class ModelLoader:
    """Class to load and manage models for embeddings and language processing.  
    It initializes the models based on configuration settings and provides methods to validate the environment."""
    def __init__(self):
        try:
            load_dotenv()
            self.config = load_config()
            self._validate_env()
           
        except Exception as e:
            log.error(f"Error in ModelLoader initialization: {e}")
            raise CustomException(e, sys)
        log.info("ModelLoader initialized successfully.")


    def _validate_env(self):
        models = ["GROQ_API_KEY", "GOOGLE_API_KEY"]
        models_keys = {model:os.getenv(model) for model in models}
        for model,key in models_keys.items():
            if key is None:
                log.error(f"Environment variable {model} is not set or provide api keys.")
                raise CustomException(f"Environment variable {model} is not set or provide api keys.", sys)
        

    def load_embedding(self):
        """Loads the embedding model based on the configuration settings."""
        try:
          model_name = self.config.get("embedding_model", "google")
          if not model_name:
                raise CustomException("Embedding model configuration is missing.", sys)
          log.info(f"Loading embedding model: {model_name}")
          if model_name.get('provider') == "google":
              return GoogleGenerativeAIEmbeddings(
                  model=model_name.get("model"),
                  max_retries=3,
                  max_tokens=model_name.get("max_tokens",4096)
              )
          elif model_name.get('provider') == "groq":
              return ChatGroq(
                  model=self.config.get["groq_embedding_model"],
                  max_retries=3,
                  max_tokens=self.config["max_tokens"]
              )
          else:
              raise CustomException(f"Unsupported embedding model: {self.config['embedding_model']}", sys)
          log.info(f"Embedding model {model_name} loaded successfully.")
        except Exception as e:
            log.error(f"Error loading embedding model: {e}")
            raise CustomException(e, sys)

    def load_llm(self):
        """Loads the language model based on the configuration settings."""

        llm_block = self.config["llm"]
        provider_ = os.getenv("LLM_PROVIDER", "google") 
        provider = llm_block.get(provider_,"google")
        if provider_ not in llm_block:
            log.error(f"LLM provider {provider} not found in configuration.")
            raise CustomException(f"LLM provider {provider} not found in configuration.", sys)
        
        
        provider_name = provider.get("provider")
        model_name = provider.get("model_name")
        temperature = provider.get("temperature", 0.2)
        max_tokens = provider.get("max_output_tokens", 2048)

        
        log.info(f"Loading LLM model: {model_name}")
        if provider_name == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                max_retries=3,
                max_tokens= max_tokens,
                temperature=temperature,
                )
        elif provider_name == "groq":
            return ChatGroq(
                model=model_name,
                max_retries=3,
                max_tokens= max_tokens,
                temperature=temperature,
                )
        else:
            raise CustomException(f"Unsupported LLM model: {self.config['llm_model']}", sys)
            log.info(f"LLM model {model_name} loaded successfully.")
     


#if __name__ == "__main__":
 #   loader = ModelLoader()
  #  embed = loader.load_embedding()