import os
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
import fitz
import uuid
import datetime

log = CustomLogger().get_logger(__name__)


class DataIngestion:

    def __init__(self,dir_path,session_id):
        """Initialize the DataIngestion class with file path and session ID.
        :param file_path: Path to the PDF file to be processed.
        :param session_id: Unique identifier for the session.  
        """
        try:
          self.dir_path = dir_path or os.getenv("DEFAULT_FILE_PATH",os.path.join(os.getcwd(), "data","archive.pdf"))
          self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

          new_dir_path = os.path.join(self.dir_path,self.session_id)
          self.new_file = os.makedirs(new_dir_path, exist_ok=True)
          log.info(f"Directory created at: {new_dir_path}")

        except:
            log.error(f"Error initializing DataIngestion with file path: {dir_path} and session ID: {session_id}")
            raise CustomException("Failed to initialize DataIngestion", sys)
                                  

        log.info(f"DataIngestion initialized at: {new_file} ")


    def save_pdf(self,file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")

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
        self.file_path = file_path
        try:
            data_block = [" "]
            with fitz.open(self.file_path, "rb") as pdf_document:
                for page in pdf_document:
                    data_block.append(page.get_text())

            content = "\n".join(data_block)
            if not content.strip():
                raise ValueError("PDF file is empty or could not be read.")

            log.info(f"PDF read successfully from: {self.file_path}")
            return content
        except Exception as e:
            log.error(f"Error reading PDF file: {e}")
            raise CustomException(f"Error reading PDF file: {e}", sys)
        

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    
    pdf_path=r"C:\\Users\\sunny\\document_portal\\data\\document_analysis\\sample.pdf"
    class DummnyFile:
        def __init__(self,file_path):
            self.name = Path(file_path).name
            self._file_path = file_path
        def getbuffer(self):
            return open(self._file_path, "rb").read()
        
    dummy_pdf = DummnyFile(pdf_path)
    
    handler = DocumentHandler()
    
    try:
        saved_path=handler.save_pdf(dummy_pdf)
        print(saved_path)
        
        content=handler.read_pdf(saved_path)
        print("PDF Content:")
        print(content[:500])  # Print first 500 characters of the PDF content
        
    except Exception as e:
        print(f"Error: {e}")
    