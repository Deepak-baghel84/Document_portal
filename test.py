import os
from pydoc import text 
from src.document_compare.document_comparator import DocumentComparatorLLM
from src.document_ingestion.data_ingestion import DocumentComparator 
from exception.custom_exception import CustomException
from pathlib import Path

act_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Deepak_Baghel_Resume.pdf')
ref_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Resume.pdf')



class DummyFile():
    """A dummy file class to simulate file operations for testing purposes."""
    def __init__(self,file_path: Path):
        self.name = Path(file_path).name
        self._read_buffer = file_path.read_bytes()
    def getbuffer(self):
        return self._read_buffer  
        
if __name__ == "__main__":
        
    try:
        act_file = DummyFile(act_path)
        ref_file = DummyFile(ref_path)
        print(f"Dummy PDF created with name: {act_file.name}")
        file_handler = DocumentComparator()
        save_pdf_path = file_handler.save_pdf_files(ref_file,act_file)
        print(f"PDFs saved at: {save_pdf_path}") 
        text_content = file_handler.combine_pdf_text()
        print(f"Content read from PDFS: {text_content[:100]}...")  # Print first 100 characters for brevity

        compare_handler = DocumentComparatorLLM()
        df = compare_handler.Document_compare(text_content)
        print(f"Comparison DataFrame: {df.head()}")  # Print first few rows of the DataFrame
        
    except CustomException as e:
        print(f"An error occurred: {e}")


     

