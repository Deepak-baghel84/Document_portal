import os
import sys
from dotenv import load_dotenv

from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from utills.config_util import load_config

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq

log = CustomLogger().get_logger(__name__)






class ModelLoader:
    def __init__(self):
        pass

    def validate_env(self):
        pass

    def load_embedding(self):
        pass

    def load_llm(self):
        pass