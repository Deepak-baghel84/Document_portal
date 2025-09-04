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
