from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_analyzer import Prompt_directory
from utills.model_utils import ModelLoader
from model.base_model import SummaryResponse,PromptType
import sys
import pandas as pd
from dotenv import load_dotenv


class DocumentCompare:
    def __init__(self):
        try:
          load_dotenv()
          self.log = CustomLogger.get_logger(__name__)
          self.loader = ModelLoader()
          self.llm = self.loader.load_llm()
          self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
          self.fixing_parser = OutputFixingParser.from_llm(
              parser=self.parser,
              llm=self.llm
          )
          self.parser = JsonOutputParser(pydantic_object=PromptType)
          self.prompt = Prompt_directory[f"PromptType.DOCUMENT_COMPARISON.value"]
          self.chain = self.prompt | self.llm | self.parser
          self.log.info("DocumentCompare initialized successfully.")
        except Exception as e:
            self.log.error(f"Error initializing DocumentCompare: {e}")
            raise CustomException("Error in initialization of DocumentCompare file", sys)
           
    def Document_compare(self,combined_text:str)->pd.Dataframe:
        try:
            inputs = {"combined_docs":combined_text ,
                      "format_instruction":self.parser.get_format_instructions()}
        
            response = self.chain.invoke(inputs)
            self.log(f"Document comparision have completed successfully.")
            self._format_response(response)
        except Exception as e:
            self.log(f"Document comparision have an issue: {e}")
            raise CustomException("Document_compare have an issue ",sys)


    def _format_response(self,response_parsed:str)->pd.DataFrame:
        try:
            df = pd.DataFrame(response_parsed)
            return df
        except Exception as e:
            self.log.error("Error formatting response into DataFrame", error=str(e))
            CustomException("Error formatting response", sys)