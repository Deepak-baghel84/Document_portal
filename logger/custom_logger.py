import os
import logging
import datetime
import structlog

class CustomLogger:
    def __init__(self,log_dir='logs'):
        """
        Initialize the custom logger.
        
        :param log_dir: Directory where log files will be stored.
        """
        log_file = os.path.join(os.getcwd(), log_dir)
        os.makedirs(log_file, exist_ok=True)
        
        # Create a log file with the current date and time
        log_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.log_file_path = os.path.join(log_file, log_file_name)
        

        
    def get_logger(self, name=__file__):
        """
        Get a logger with the specified name.
            
        :param name: Name of the logger as current working file.
        """
        logger_name = os.path.basename(name)             # Get the base name of the file


        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(message)s'))

        #  logging for console output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(' %(message)s'))
    

        
        # Configure structlog for structured logging file
        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            handlers=[
                file_handler,
                console_handler
            ]
        )

          # configure logging for console

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt='iso',utc = True,key='timestamp'),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to = 'event'),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True
        )
        return structlog.get_logger(logger_name)
        
#if __name__ == "__main__":
    # Example usage
#    logger = CustomLogger().get_logger(__file__)
#    logger.info("User uploaded a file", user_id=123, filename="report.pdf")
#    logger.error("Failed to process PDF", error="File not found", user_id=123)
    
    