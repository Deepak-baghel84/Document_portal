import os
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
import fitz
import uuid
import datetime

log = CustomLogger().get_logger(__name__)


class DataIngestion:

    def __init__(self,file_path,session_id):
        """Initialize the DataIngestion class with file path and session ID.
        :param file_path: Path to the PDF file to be processed.
        :param session_id: Unique identifier for the session.  
        """
        try:
          self.file_path = file_path or os.getenv("DEFAULT_FILE_PATH",os.path.join(os.getcwd(), "data","archive.pdf"))
          self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

          dir_path = os.path.join(self.file_path,self.session_id)
          new_file = os.makedirs(dir_path, exist_ok=True)
          log.info(f"Directory created at: {dir_path}")

        except:
            log.error(f"Error initializing DataIngestion with file path: {file_path} and session ID: {session_id}")
            raise CustomException("Failed to initialize DataIngestion", sys)
                                  

        log.info(f"DataIngestion initialized with file: {self.file_name}")

    def read_pdf(self):
        pass

    def save_pdf(self):
        pass