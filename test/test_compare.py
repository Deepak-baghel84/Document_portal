import os 
from src.doc_analyzer.data_analysis import DataAnalysis
from src.doc_compare.ingestion import Ingestor 
from exception.custom_exception import CustomException
from logger.custom_logger import CustomLogger
from pathlib import Path


act_path = Path('c:\\Genai_projects\\Document_portal\\Data\\sample.pdf')
ref_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Resume.pdf')



class DummyFile():
    """A dummy file class to simulate file operations for testing purposes."""
    def __init__(self,file_path: Path):
        self.name = Path(file_path).name
        self._read_buffer = file_path.read_bytes()
    def get_buffer(self):
        return self._read_buffer  
        
if __name__ == "__main__":
        
    try:
        act_file = DummyFile(act_path)
        ref_file = DummyFile(ref_path)
        print(f"Dummy PDF created with name: {act_file.name}")
        file_handler = Ingestor(base_dir ="data//archive_compare" )
        save_pdf_path = file_handler.save_pdf_files(ref_file,act_file)
        print(f"PDFs saved at: {save_pdf_path}") 
        text_content = file_handler.combine_pdf_text()
        print(f"Content read from PDFS: {text_content[:100]}...")  # Print first 100 characters for brevity
        
    except CustomException as e:
        print(f"An error occurred: {e}")


     

