from src.doc_ingestion.data_ingestion import (
    AnalyzeIngestor,
    CompareIngestor,
    DocumentIngestor,
)
from src.doc_analyzer.analyzer import DataAnalysis
from src.doc_compare.file_compare import DocumentCompare
from src.doc_chat.doc_retriver import DocumentRetriever
#from utills.document_ops import FastAPIFileAdapter,read_pdf_via_handler
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from pathlib import Path
import sys
import os 

from typing import List, Optional, Any, Dict
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


FAISS_BASE = os.getenv("FAISS_BASE", "faiss_index")
UPLOAD_BASE = os.getenv("UPLOAD_BASE", "data")
FAISS_INDEX_NAME = os.getenv("FAISS_INDEX_NAME", "index")  # <--- keep consistent with save_local()

app = FastAPI(title="Document Portal API", version="0.1")

# connect static files
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
app.mount("/static", StaticFiles(directory=(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check()-> Dict[str,str]:
    return {"status": "ok", "message": "Service is healthy","device": "document-portal"}

@app.post("/analyze")
async def analyze_document():
    pass

@app.post("/compare")
def compare_documents():
    pass

@app.post("/chat/ingest")
def chat_ingest():
    pass

@app.post("/chat/query")
def chat_query():
    pass