from pathlib import Path
import yaml
from dotenv import load_dotenv

load_dotenv()


def load_config(config_path="config/config.yaml"):
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
