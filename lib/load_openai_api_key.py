import os
import re

def load_openai_api_key():
    config_relative_path = "config/api_key.txt"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, config_relative_path)

    fallback_path = os.path.expanduser("~/.openai/api_key.txt")

    key = None
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            key = f.read().strip()
    elif os.path.exists(fallback_path):
        with open(fallback_path, "r") as f:
            key = f.read().strip()

    if key is None:
        raise FileNotFoundError("API key not found in config/ or ~/.openai/ directories.")
    
    if not re.fullmatch(r"[\w\-]{50,}", key):
        raise ValueError("Invalid API key format. It must be at least 50 characters and contain only alphanumerics and '-'.")

    return key