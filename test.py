import os
from pydoc import text 
from src.doc_compare.file_compare import DocumentCompare
from src.doc_compare.file_compare import DocumentCompare
from src.doc_ingestion.data_ingestion import CompareIngestor 
from exception.custom_exception import CustomException
from pathlib import Path

act_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Deepak_Baghel_Resume.pdf')
ref_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Resume.pdf')




        
if __name__ == "__main__":
        
    try:
    
        file_handler = CompareIngestor()
        save_pdf_path = file_handler.save_pdf_files(ref_path,act_path)
        print(f"PDFs saved at: {save_pdf_path}") 
        text_content = file_handler.combine_pdf_text()
        print(f"Content read from PDFS: {text_content[:100]}...")  # Print first 100 characters for brevity

        compare_handler = DocumentCompare()
        df = compare_handler.Document_compare(text_content)
        print(f"Comparison DataFrame: {df.head()}")  # Print first few rows of the DataFrame
        
    except CustomException as e:
        print(f"An error occurred: {e}")


     

