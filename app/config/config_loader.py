from dependency_injector import providers
from app.utils.data_loader import DataLoader

class ConfigLoader:
    def __init__(self, global_env_file):
        self.global_env = DataLoader.load_json(global_env_file)
        self._config = {}
        self._load_yaml_config()

    def _load_yaml_config(self):
        """Loads configuration from YAML models, prioritizing environment variables."""

        # Load base config
        properties_path = self.global_env["paths"]["properties"] + "yaml/"
        base_config = self.global_env["files"]["properties_config"]["base_config"]
        base_config = DataLoader.load_yaml(properties_path+base_config)

        # Determine environment
        env = base_config["environment"]["active"]
        env_config = self.global_env["files"]["properties_config"][env]
        env_config = DataLoader.load_yaml(properties_path+env_config)

        # Merge base and environment-specific structures
        self._config = {**base_config, **env_config}

    def load_config_provider(self):
        config = providers.Configuration()
        config.from_dict(self._config)
        return config

    def get_config_dict(self):
        """Return config dictionary"""
        return self._config
