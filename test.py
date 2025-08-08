import os 
from src.doc_analyzer.data_analysis import DataAnalysis
from src.doc_analyzer.data_ingestion import DataIngestion
from exception.custom_exception import CustomException
from logger.custom_logger import CustomLogger
from pathlib import Path

pdf_path='c:\\Genai_projects\\Document_portal\\Data\\sample.pdf'

class DummnyFile:
    def __init__(self,file_path):
        self.name = Path(file_path).name
        self._file_path = file_path
    def getbuffer(self):
        return open(self._file_path, "rb").read()
def main():
    """Main function to run the data analysis on a sample PDF."""
    try:
        dummy_pdf = DummnyFile(pdf_path)
        print(f"Dummy PDF created with name: {dummy_pdf.name}")
        file_handler = DataIngestion(session_id="test_session")
        save_pdf_path = file_handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {save_pdf_path}") 
        text_content = file_handler.read_pdf(save_pdf_path)
        print(f"Content read from PDF: {text_content[:100]}...")  # Print first 100 characters for brevity
        
        data_analysis = DataAnalysis()
        analysis_result = data_analysis.analyze_document(text_content)
        print("Analysis Response:", analysis_result)
        for key, value in analysis_result.items():
            print(f"{key}: {value}")
        
    except CustomException as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()