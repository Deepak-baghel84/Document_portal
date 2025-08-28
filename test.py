import os 
from src.doc_ingestion.data_ingestion import DocumentIngestor
from src.doc_chat.doc_retriver import DocumentRetriever
from exception.custom_exception import CustomException
from pathlib import Path
import sys





def test_doc_chat():
    try:
        file_paths = ["Data//Resume.pdf","Data//Sample.pdf","Data//Deepak_Baghel_Resume.pdf"]
       
        ingestor = DocumentIngestor(file_path="Data//multidoc_archive",faiss_index_path="vector_store")
        uploaded_files = []
        for file_path in file_paths:
             if Path(file_path).exists():
                 uploaded_files.append(open(file_path, "rb"))  # to perform read operation adding file path in open mode
             else:
                 print(f"File does not exist: {file_path}")
            
        documents = ingestor.ingest_file(uploaded_files)
  
        retriver = ingestor.create_retrivel(documents)
     #   doc_retriver = DocumentRetriever(retriver=retriver)
     #   for file in uploaded_files:
      #      file.close()
     #   answer = doc_retriver.invoke(user_query="What is the document about?")
     #   print(answer)
    except Exception as e:
        raise CustomException(e,sys)
    

if __name__ == "__main__":
    test_doc_chat()