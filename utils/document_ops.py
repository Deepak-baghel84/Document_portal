from __future__ import annotations
from pathlib import Path
import os
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
        for file_path in file_paths :
            log.info(f"Loading document from path: {file_path}")
            file_name = os.path.basename(file_path.name)
            if Path(file_name).suffix.lower() not in SUPPORTED_EXTENSIONS:
                log.error(f"Unsupported file format: {Path(file_name).suffix}")
                continue

            if file_name.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_name.suffix.lower() == ".docx":
                loader = Docx2txtLoader(str(file_path))
            elif file_name.suffix.lower() == ".txt":
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
    


def save_pdf_via_handler(file:UploadFile,save_dir:Path)-> Path:
    try:
        if not file:
            raise CustomException("No file provided", None)
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)
        file_name = os.path.basename(file.filename)
        if Path(file_name).suffix.lower() != ".pdf":
            log.error(f"Unsupported file format: {Path(file_name).suffix}")
            raise CustomException(f"Unsupported file format: {Path(file_name).suffix}", None)
        save_path = save_dir / file_name
        with open(save_path, 'wb') as f:
            f.write(file.file.read())
        log.info(f"File saved successfully at: {save_path}")
        return save_path
    except Exception as e:
        log.error(f"Error saving file: {e}")
        raise CustomException(f"Error saving file: {e}", None)
    




class FastAPIFileAdapter:
    """Adapt FastAPI UploadFile -> .name + .getbuffer() API"""
    def __init__(self, uf: UploadFile):
        self._uf = uf
        self.name = uf.filename
    def getbuffer(self) -> bytes:
        self._uf.file.seek(0)
        return self._uf.file.read()


def read_pdf_via_handler(handler, path: str) -> str:
    if hasattr(handler, "read_pdf"):
        return handler.read_pdf(path)  # type: ignore
    if hasattr(handler, "read_"):
        return handler.read_(path)  # type: ignore
    raise RuntimeError("DocHandler has neither read_pdf nor read_ method.")