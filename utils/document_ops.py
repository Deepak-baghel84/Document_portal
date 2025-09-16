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
        
            doc = loader.load()
            docs.extend(f"Document: {file_name}\n{d.page_content}" for d in doc)
        log.info(f"Loaded {len(docs)} pages successfully")
        return docs
    except Exception as e:
        log.error(f"Error loading document : {e}")
        raise CustomException(f"Error loading document : {e}", None)
    
def concat_for_analysis(docs: List[Document]) -> str:
    parts = []
    for d in docs:
        src = d.metadata.get("source") or d.metadata.get("file_path") or "unknown"
        parts.append(f"\n--- SOURCE: {src} ---\n{d.page_content}")
    return "\n".join(parts)

def concat_for_comparison(ref_docs: List[Document], act_docs: List[Document]) -> str:
    left = concat_for_analysis(ref_docs)
    right = concat_for_analysis(act_docs)
    return f"<<REFERENCE_DOCUMENTS>>\n{left}\n\n<<ACTUAL_DOCUMENTS>>\n{right}"

#---------- Helper Classes and Functions ----------
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