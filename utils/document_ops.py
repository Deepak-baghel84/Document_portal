from __future__ import annotations
from pathlib import Path
from typing import Iterable, List
from fastapi import UploadFile
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def load_document(file_paths:Iterable[Path])-> List[Document]:
    docs: List[Document] = []
    try:
        for file_path in file_paths if isinstance(file_paths, Iterable) else [file_paths]:
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix.lower() == ".docx":
                loader = Docx2txtLoader(str(file_path))
            elif file_path.suffix.lower() == ".txt":
                loader = TextLoader(str(file_path), encoding="utf-8")
            else:
                log.error(f"Unsupported file format: {file_path.suffix}")
                raise CustomException(f"Unsupported file format: {file_path.suffix}", None)
        
            docs.extend(loader.load())
        log.info(f"Loaded {len(docs)} pages successfully")
        return docs
    except Exception as e:
        log.error(f"Error loading document : {e}")
        raise CustomException(f"Error loading document : {e}", None)