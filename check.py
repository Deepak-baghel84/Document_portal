from utills.config_util import load_config
import os
from logger.custom_logger import CustomLogger
import datetime


##    checking the config by loading it
#def test_load_config():
  #      config = load_config()
   #     llm_block = config["llm"]
    #    provider_ = os.getenv("LLM_PROVIDER", "google")
     #   provider = llm_block.get(provider_, "google")
   #
#
 #       provider_name = provider.get("provider")
  #      model_name = provider.get("model_name")
   #     temperature = provider.get("temperature", 0.2)
    #   print(f"Provider: {provider_name}, Model: {model_name}, Temperature: {temperature}, Max Tokens: {max_tokens}")
#
#test_load_config()


def test_log(log_dir='log'):
        """
        Initialize the custom logger.
        
        :param log_dir: Directory where log files will be stored.
        """
        log_file = os.path.join(os.getcwd(), log_dir)
        os.makedirs(log_file, exist_ok=True)
        print(log_file)
        
        # Create a log file with the current date and time
        log_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        print(log_file_name)
        log_file_path = os.path.join(log_file, log_file_name)
        print(log_file_path)
    

test_log()