import os
import logging
from dynaconf import Dynaconf
from pathlib import Path

class ConfigManager:
    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.config_dir = Path("/home/samiksha889/project/config_manager/config")
        self.secrets_path = self.config_dir / "secrets.yaml"

        self.config = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=[
                self.config_dir / "cloud.yaml",
                self.config_dir / "app.yaml",
                self.config_dir / "database.yaml",
                self.secrets_path
            ]
        )

        self.validate_required_keys()
        self.validate_types()
        self.check_api_key()
        self.check_secrets_file()
        self.check_domain_mappings()
        self.check_domain_config()
        self.log_loaded_config()
        self.read_config()

    def validate_required_keys(self):
        required_keys = [
            "cloud_details", "database_details", "model_type",
            "features", "cloud_secrets"
        ]
        for key in required_keys:
            if not hasattr(self.config, key):
                raise ValueError(f"Missing required config key: {key}")
        print("✅ All required keys are present.")

    def validate_types(self):
        if not isinstance(self.config.model_type, str):
            raise TypeError("model_type must be a string")

        if not isinstance(self.config.database_details.sample_domain.port, int):
            raise TypeError("Database port must be an integer")

        if not isinstance(self.config.cloud_details.sample_domain.provider, str):
            raise TypeError("Provider must be a string")

        if not isinstance(self.config.features.enable_feature_x, bool):
            raise TypeError("Feature flag must be a boolean")

        if not isinstance(self.config.cloud_secrets.sample_domain.api_key, str):
            raise TypeError("API key must be a string")

        print("✅ All type checks passed successfully.")

    def check_api_key(self):
        api_key = getattr(self.config.cloud_secrets, "sample_domain", {}).get("api_key")
        if not api_key or api_key == "REPLACE_ME":
            raise ValueError("Missing or placeholder API key for cloud provider")
        print("✅ API key is valid.")

    def check_secrets_file(self):
        if not self.secrets_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.secrets_path}")
        print(f"✅ Secrets file found: {self.secrets_path}")

    def check_domain_mappings(self):
        cloud_domains = self.config.cloud_details.to_dict().keys()
        db_domains = self.config.database_details.to_dict().keys()
        missing_in_cloud = set(db_domains) - set(cloud_domains)
        if missing_in_cloud:
            raise ValueError(f"Domains in DB config missing in cloud config: {missing_in_cloud}")
        print("✅ Cloud and DB domain mappings are consistent.")

    def check_domain_config(self):
        if not hasattr(self.config.database_details, self.domain_name):
            raise ValueError(f"No DB config for domain: {self.domain_name}")
        print(f"✅ Domain '{self.domain_name}' is present in database config.")

    def log_loaded_config(self):
        log_level = self.config.get("log_level", "INFO").upper()
        logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
        logging.info(f"Loaded config for domain: {self.domain_name}, model: {self.config.model_type}")
        
    def read_config(self):
        print("📦 Provider:", self.config.cloud_details.sample_domain.provider)
        print("🌍 Region (model_type):", self.config.model_type)
        print("✅ Feature Enabled:", self.config.features.enable_feature_x)
        print("🔑 API Key:", self.config.cloud_secrets.sample_domain.api_key)


# 🧪 Run with example domain name
if __name__ == "__main__":
    os.environ["ENV_FOR_DYNACONF"] = "production"  # Set env var
    ConfigManager(domain_name="sample_domain")