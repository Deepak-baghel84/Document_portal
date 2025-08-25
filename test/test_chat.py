import os 
from src.Document_chat.retriver import DocumentRetriever
from src.Document_chat.ingestion import DocumentIngestor
from exception.custom_exception import CustomException
from logger.custom_logger import CustomLogger
from pathlib import Path
import sys



file_paths = ["Data//Resume.pdf","Data//Sample.pdf","Data//Deepak_Baghel_Resume.pdf"]

def test_doc_chat(file_paths):
    try:
        log = CustomLogger.get_logger(__name__)
        log.info("test_doc_chat started")
        ingestor = DocumentIngestor(file_path="Data//multidoc_archive",faiss_index_path="vector_store")
        uploaded_files = []
        for file_path in file_paths:
            with open (file_path,"rb") as f:
                uploaded_files.append(f)
            
        documents = ingestor.ingest_file(uploaded_files)
        for file in uploaded_files:
            file.close()
        
        retriver = ingestor.create_retrivel(documents)
        doc_retriver = DocumentRetriever(retriver=retriver)
        answer = doc_retriver.invoke(user_query="What is the document about?")
        log.info("test_doc_chat completed successfully")
        print(answer)
    except Exception as e:
        log.error("Error in test_doc_chat")
        raise CustomException(e,sys)
    

if __name__ == "__main__":
    test_doc_chat(file_paths)
