import yaml
from logger import GLOBAL_LOGGER  as log


def load_config(file_path:str = "config\config.yaml") -> dict:
    """
    Load configuration from a YAML file.
    
    :param file_path: Path to the YAML configuration file.
    :return: Dictionary containing the configuration.
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    log.debug(f"Configuration content: {config}")
    return config

#if __name__ == "__main__":
 #   config = load_config()
  #  print(config)


#  load config output in json format
#   {'app': {'name': 'DocumentPortal', 'version': '1.0.0', 'description': 'A portal for comparing,analyzing or making a chat with documents using AI.'}, 'logging': {'level': 'INFO', 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}, 'database': {'provider': 'sqlite', 'connection_string': 'sqlite:///./database.db'}, 'document': {'provider': 'local'}, 'embedding_model': {'provider': 'google', 'model': 'models/text-embedding-004'}, 'llm': {'groq': {'provider': 'groq', 'model': 'deepseek-r1-distill-llama-70b', 'temperature': 0.2, 'max_output_tokens': 2048}, 'google': {'provider': 'google', 'model_name': 'gemini-1.5-flash', 'temperature': 0.2, 'max_output_tokens': 2048}}, 'retriever': {'top_k': 10}, 'vector_store': {'provider': 'chromadb', 'collection_name': 'document_collection', 'persist_directory': './vector_store'}} 