import os 
from src.document_ingestion.data_ingestion import ChatIngestor
from src.document_chat.retrieval import ConversationalRAG
from exception.custom_exception import CustomException
from pathlib import Path
import sys


def test_doc_chat():
    try:
        file_paths = ["Data//Resume.pdf","Data//Sample.pdf","Data//Deepak_Baghel_Resume.pdf"]
       
        ingestor = ChatIngestor(file_path="Data//multidoc_archive", faiss_base = "faiss_index",use_session_dirs = True,session_id= None)
        uploaded_files = []
        for file_path in file_paths:
             if Path(file_path).exists():
                 uploaded_files.append(open(file_path, "rb"))  # to perform read operation adding file path in open mode
             else:
                 print(f"File does not exist: {file_path}")
            
        documents = ingestor.ingest_file(uploaded_files)
  
        retriver = ingestor.create_retrivel(document=documents,chunk_size= 1000,chunk_overlap= 200,k= 5)
        doc_retriver = ConversationalRAG(retriver=retriver)
        for file in uploaded_files:
            file.close()
        answer = doc_retriver.Invoke(user_query="What is the documents about?")
        print(answer)
    except Exception as e:
        pass
       # raise CustomException(e,sys)
    

if __name__ == "__main__":
    test_doc_chat()