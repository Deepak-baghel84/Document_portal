import os
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
from pypdf import PdfReader
from datetime import datetime
import sys  
from pathlib import Path

log = CustomLogger().get_logger(__name__)


class Ingestor(base_dir=None,session_file=None):
    """Class to handle PDF ingestion and processing.
    It reads PDF files, extracts text, and manages file paths."""
    
    def __init__(self, base_dir=None, session_file=None):
        try:
            self.base_dir = base_dir or os.getenv("DEFAULT_FILE_PATH", os.path.join(os.getcwd(), "data", "archive_pdfs"))
            self.base__dir = Path(self.base_dir)
            self.sessionn_file = session_file or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_path =  self.base_dir / self.sessionn_file
            self.session_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.log.error(f"Error initializing Ingestor: {e}")
            raise CustomException(e, sys)
        

    def save_pdf_files(self, ref_file,act_file):
        """Save the PDF files to the specified directory.
        :param ref_file: Path to the reference PDF file.
        :param act_file: Path to the actual PDF file.
        :return: Paths where the PDF files are saved.
        """
        try:
            self.ref_file = Path(ref_file)
            self.act_file = Path(act_file)
            if not self.ref_file.name.lower().endswith('.pdf') or not self.act_file.name.lower().endswith('.pdf'):
                raise ValueError("One or both files are not PDFs.")
            ref_save_path = self.session_path / self.ref_file.name
            act_save_path = self.session_path / self.act_file.name
            with open(ref_save_path, 'wb') as file:
                file.write(self.ref_file.get_buffer())
            with open(act_save_path, 'wb') as file:
                file.write(self.act_file.get_buffer())
            log.info(f"PDF files saved successfully at: {self.session_path}")
            return ref_save_path, act_save_path

        except FileNotFoundError as e:
            log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)

    def read_pdf(self, file_path:Path):
        """Read the PDF file and return its content.
        :param file_path: Path to the PDF file to be read.
        :return: Text content of the PDF file.
        """
        try:
            data_block = []
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text.strip():
                        data_block.append(f"Page ---{page.number + 1}---:\n{text.strip()}")
                       
            if not data_block:
                raise ValueError("No text found in the PDF file.")
            
            self.log.info(f"PDF read successfully from: {file_path}")
            if data_block.strip():
                raise ValueError("PDF file is empty or could not be read.")
            return "\n".join(data_block)
        except FileNotFoundError as e:
            self.log.error(f"File not found: {e}")
            raise CustomException(f"File not found: {e}", sys)
        

    def combine_pdf_text(self):
        """Combine the text from the reference and actual PDF files.
        :param ref_text: Text content of the reference PDF file.
        :param act_text: Text content of the actual PDF file.
        :return: Combined text content.
        """
        try:
            doc_block = []
            for pdf_file in sorted(self.session_path.iterdir()):
                if pdf_file.suffix.lower() == '.pdf':
                    content = self.read_pdf(pdf_file)
                    doc_block.append(content)
            combined_text = "\n".join(doc_block)
            if not combined_text.strip():
                raise ValueError("No text found in the PDF files.")
            log.info("PDF text combined successfully.")
            return combined_text
        except Exception as e:
            log.error(f"Error combining PDF text: {e}")
            raise CustomException(e, sys)
        


    def remove_pdf_files(self):
        """Remove the PDF files from the session directory."""
        try:
            for pdf_file in self.session_path.iterdir():
                if pdf_file.suffix.lower() == '.pdf':
                    pdf_file.unlink()
            self.session_path.rmdir()  # Remove the session directory if empty
            self.log.info(f"Old PDF files and folder removed successfully from: {self.session_path}")
                
        except Exception as e:
            log.error(f"Error removing PDF files: {e}")
            raise CustomException(e, sys)