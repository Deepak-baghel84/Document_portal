from utills.config_util import load_config
import os



def test_load_config():
        config = load_config()
        llm_block = config["llm"]
        provider_ = os.getenv("LLM_PROVIDER", "google")
        provider = llm_block.get(provider_, "google")
   

        provider_name = provider.get("provider")
        model_name = provider.get("model_name")
        temperature = provider.get("temperature", 0.2)
        max_tokens = provider.get("max_output_tokens", 2048)
        print(f"Provider: {provider_name}, Model: {model_name}, Temperature: {temperature}, Max Tokens: {max_tokens}")

test_load_config()