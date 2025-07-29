import os
import logging
import datetime

class CustomLogger:
    def __init__(self, log_dir='log'):
        """
        Initialize the custom logger.
        
        :param log_dir: Directory where log files will be stored.
        """
        log_file = os.path.join(os.getcwd(), log_dir)
        os.makedirs(log_file, exist_ok=True)
        
        # Create a log file with the current date
        log_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        log_file_path = os.path.join(log_file, log_file_name)
        
        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            format='[%(asctime)s] - %(levelname)s - %(name)s (line:%(lineno)d) - %(message)s',
            level=logging.INFO,
        )
    def get_logger(self, name=__file__):
        """
        Get a logger with the specified name.
            
        :param name: Name of the logger as current working file.
        :return: Configured logger instance.
        """
        logger = logging.getLogger(os.path.basename(name)) 
        return logger
        
if __name__ == "__main__":
    # Example usage
    custom_logger = CustomLogger()
    logger = custom_logger.get_logger(__file__)
    
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    
    