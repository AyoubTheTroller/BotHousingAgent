from pathlib import Path
import json
import yaml

class DataLoader:

    # Default root path is the project's root directory
    BASE_PATH = Path(__file__).parent.parent.parent

    @staticmethod
    def _resolve_path(file_path: str) -> Path:
        """Resolves a file path to an absolute path."""
        path = Path(file_path)
        if not path.is_absolute():
            # If the path is relative, resolve it against the base path
            path = DataLoader.BASE_PATH / path
        return path

    @classmethod
    def load_json(cls, file_path: str) -> dict:
        """Loads and parses a JSON file."""
        config_path = cls._resolve_path(file_path)
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"JSON file not found: {config_path}") from FileNotFoundError

    @classmethod
    def load_yaml(cls, file_path: str) -> dict:
        """Loads and parses a YAML file."""
        config_path = cls._resolve_path(file_path)
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise ValueError(f"YAML file not found: {config_path}") from FileNotFoundError

    @staticmethod
    def get_value_by_key_path(data: dict, key_path: list[str]):
        """Retrieves a value from a dictionary (loaded JSON/YAML data) using a list of keys."""
        value = data
        for key in key_path:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                raise ValueError(f"Key '{key}' not found in path: {key_path}")
        return value
