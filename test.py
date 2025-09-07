import os
from pydoc import text 
from src.doc_analyzer.analyzer import DataAnalysis
from src.doc_ingestion.data_ingestion import AnalyzeIngestor 
from exception.custom_exception import CustomException
from pathlib import Path

pdf_path = Path('c:\\Genai_projects\\Document_portal\\Data\\Deepak_Baghel_Resume.pdf')


def main():
#    """Main function to run the data analysis on a sample PDF."""
    try:
        #dummy_pdf = DummnyFile(pdf_path)
        print(f"Dummy PDF created ")
        file_handler = AnalyzeIngestor(session_id="test_session")
        save_file = file_handler.save_pdf(uploaded_files=pdf_path)
        
        text_content = file_handler.read_pdf()
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

