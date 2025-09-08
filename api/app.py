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
async def analyze_document(file:UploadFile=File(...))-> JSONResponse:
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
async def compare_documents(act_path:UploadFile=File(...),ref_path:UploadFile=File(...))-> Dict[str, Any]:
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
async def chat_ingest(files:List[UploadFile]=File(...),session_id: Optional[str] = Form(None),use_session_dirs:bool=Form(True),k: int = Form(5),chunk_size: int = Form(512),chunk_overlap: int = Form(50))->Any:
    try:
        wrapped = [file for file in files]
        log.info(f"Received files for chat ingestion")
        if wrapped is None or len(wrapped) == 0:
            raise HTTPException(status_code=400, detail="No files provided")
        
        file_handler = DocumentIngestor(temp_base=UPLOAD_BASE,
            faiss_base=FAISS_BASE,
            use_session_dirs=use_session_dirs,
            session_id=session_id or None,)
        save_pdf_path = file_handler.save_pdf_files(wrapped)
        log.info(f"PDFs saved at: {save_pdf_path}")

        text_content = file_handler.combine_pdf_text()
        log.info(f"Content read from PDFs: {text_content[:100]}...")  # Print first 100 characters for brevity

        retriever = file_handler.create_retrivel(wrapped, chunk_size=chunk_size, chunk_overlap=chunk_overlap, k=k)
        return {"session_id": file_handler.session_id, "k": k, "use_session_dirs": use_session_dirs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

@app.post("/chat/query")
async def chat_query(
    question: str = Form(...),
    session_id: Optional[str] = Form(None),
    use_session_dirs: bool = Form(True),
    k: int = Form(5),
) -> Any:
    try:
        if use_session_dirs and not session_id:
            raise HTTPException(status_code=400, detail="session_id is required when use_session_dirs=True")

        # Prepare FAISS index path
        index_dir = os.path.join(FAISS_BASE, session_id) if use_session_dirs else FAISS_BASE  # type: ignore
        if not os.path.isdir(index_dir):
            raise HTTPException(status_code=404, detail=f"FAISS index not found at: {index_dir}")

        # Initialize LCEL-style RAG pipeline
        rag = DocumentRetriever(session_id=session_id) #type: ignore
        #rag.load_retriever_from_faiss(index_dir)

        # Optional: For now we pass empty chat history
        response = rag.Invoke(question, chat_history=[])

        return {
            "answer": response,
            "session_id": session_id,
            "k": k,
            "engine": "LCEL-RAG"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")