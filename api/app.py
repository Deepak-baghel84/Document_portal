from regex import A
from src import doc_compare
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
async def analyze_document(file:UploadFile=File(...)):
    try:
        log.info(f"Received file for analysis: {file.filename}")
        if not file:
            raise HTTPException(status_code=400, detail="No file provided") 
        file_dir = Path(file)
        file_handler = AnalyzeIngestor(session_id="test_session")
        save_file = file_handler.save_pdf(uploaded_files=file_dir)
        
        text_content = file_handler.read_pdf()
        
        data_analysis = DataAnalysis()
        analysis_result = data_analysis.analyze_document(text_content)
    
        return JSONResponse(content=analysis_result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@app.post("/compare")
async def compare_documents(act_path:UploadFile=File(...),ref_path:UploadFile=File(...)):
    try:
        log.info(f"Received files for comparison: {act_path.filename}, {ref_path.filename}")
        act_file = Path(act_path)
        ref_file = Path(ref_path)
   
        doc_compare = CompareIngestor()
        _ = doc_compare.save_pdf_files(ref_file,act_file)
        text_content = doc_compare.combine_pdf_text()

        compare_handler = DocumentCompare()
        df = compare_handler.Document_compare(text_content)

        return {"rows": df.to_dict(orient="records"), "session_id": doc_compare.session_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {e}")

@app.post("/chat/ingest")
def chat_ingest(file:UploadFile=File(...)):
    pass

@app.post("/chat/query")
def chat_query():
    pass