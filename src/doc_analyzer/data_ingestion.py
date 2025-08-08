import os, sys
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
import fitz
from pypdf import PdfReader
import uuid
import datetime
from pathlib import Path

log = CustomLogger().get_logger(__name__)


class DataIngestion:

    def __init__(self,dir_path=None,session_id=None):
        """Initialize the DataIngestion class with file path and session ID.
        :param file_path: Path to the PDF file to be processed.
        :param session_id: Unique identifier for the session.  
        """
        try:
          self.dir_path = dir_path or os.getenv("DEFAULT_FILE_PATH",os.path.join(os.getcwd(), "data","archive_pdfs"))
          self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

          new_dir_path = os.path.join(self.dir_path,self.session_id)
          self.new_file = os.makedirs(new_dir_path, exist_ok=True)
          log.info(f"Directory created at: {new_dir_path}")

        except:
            log.error(f"Error initializing DataIngestion with file path: {dir_path} and session ID: {session_id}")
            raise CustomException("Failed to initialize DataIngestion", sys)
                                  

    def save_pdf(self,file_path):
        """Save the PDF file to the specified directory.
        :param file_path: Path to the PDF file to be saved(passed Dummny class obj as path).
        :return: Path where the PDF file is saved.
        """
        try:
            self.file_path = file_path
            self.file_name = os.path.basename(file_path.name)

            if not self.file_name.lower().endswith('.pdf'):
                raise ValueError("File is not a PDF: {self.file_name}")
            
            save_path = os.path.join(self.dir_path, self.file_name)
            
            with open(save_path, 'wb') as file:
                file.write(self.file_path.getbuffer())

            log.info(f"PDF saved successfully at: {save_path}")
            return save_path

        except FileNotFoundError as e:
            log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)
        

    
    def read_pdf(self,file_path):
        """Read the PDF file and return its content.
        :param file_path: Path to the PDF file to be read.
        :return: Content of the PDF file as a string.
        """
        try:
            data_block = []
            num = 1
            with open(file_path, "rb") as pdf_document:
                reader = PdfReader(pdf_document)
                for page in reader.pages:
                    text = page.extract_text()
                    # Check if the page is empty or cannot be read
                    if text is None:
                        raise ValueError(f"Page {num} is empty or could not be read.")
                    # Extract text from each page
                    if text.strip():
                        data_block.append(f"\n ---Page {num}---: \n{page.extract_text()}")
                    num += 1

            if not data_block:
                raise ValueError("No text found in the PDF file.")
            log.info(f"PDF read successfully from: {file_path}")
            content = "\n".join(data_block)
            return content
        except Exception as e:
            log.error(f"Error reading PDF file: {e}")
            raise CustomException(f"Error reading PDF file: {e}", sys)
        


    
    
    
    