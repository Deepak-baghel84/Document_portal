import os
from exception import CustomException
from logger import CustomLogger
from utills.model_utils import ModelLoader
from prompt.prompt_analyzer import Prompt
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from 
import sys






class DataAnalysis:
    """Class to perform data analysis on the ingested PDF files.
    It initializes the model loader and provides methods for data analysis."""
    
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.load_model = ModelLoader()
            self.llm_model = self.load_model.load_llm()
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser,llm=self.llm_model)
            self._prompt = prompt
           
        except Exception as e:
            self.log.error(f"Error initializing DataAnalysis: {e}")
            raise CustomException(e, sys)
        
        def analyze_document(self, document_text):
            """Analyze the document text and return a structured JSON response.
            :param document_text: Text content of the document to be analyzed.
            :return: JSON response containing the analysis results.
            """
            try:
                prompt = Prompt().get_analysis_prompt()
                output_parser = JsonOutputParser()
                formatted_prompt = prompt.format(document_text=document_text)
                response = self.embedding_model(formatted_prompt)
                parsed_response = output_parser.parse(response)
                self.logger.info("Document analysis completed successfully.")
                return parsed_response
            except Exception as e:
                self.logger.error(f"Error analyzing document: {e}")
                raise CustomException(f"Error analyzing document: {e}", sys)