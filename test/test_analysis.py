
from src.document_analyzer.data_analysis import DocumentAnalyzer
from src.document_ingestion.data_ingestion import DocHandler 
from exception.custom_exception import CustomException
from pathlib import Path

pdf_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Deepak_Baghel_Resume.pdf')

class DummnyFile:
    def __init__(self,file_path):
        self.name = Path(file_path).name
        self._file_path = file_path
    def getbuffer(self):
        return open(self._file_path, "rb").read()
def main():
#    """Main function to run the data analysis on a sample PDF."""
    try:
        dummy_pdf = DummnyFile(pdf_path)
        print(f"Dummy PDF created with name: {dummy_pdf.name}")
        file_handler = DocHandler(dir_path="Data//analyzer_archive",session_id="test_session")
        save_file_path = file_handler.save_pdf(dummy_pdf)
        
        text_content = file_handler.read_pdf(save_file_path)
        print(f"Content read from PDF: {text_content[:100]}...")  # Print first 100 characters for brevity
        
        data_analysis = DocumentAnalyzer()
        analysis_result = data_analysis.analyze_document(text_content)
        print("Analysis Response:", analysis_result)
        for key, value in analysis_result.items():
            print(f"{key}: {value}")
        
    except CustomException as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()

