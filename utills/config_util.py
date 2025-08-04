import yaml

def load_config(file_path:str = "config\config.yaml") -> dict:
    """
    Load configuration from a YAML file.
    
    :param file_path: Path to the YAML configuration file.
    :return: Dictionary containing the configuration.
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
