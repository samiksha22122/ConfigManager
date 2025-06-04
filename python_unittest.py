import unittest
import os
from pathlib import Path

# Importing from config_manager.py (which is in the root)
from config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["ENV_FOR_DYNACONF"] = "production"
        cls.domain = "sample_domain"
        cls.manager = ConfigManager(domain_name=cls.domain)

    def test_model_type(self):
        self.assertEqual(self.manager.config.model_type, "gpt-like")

    def test_feature_flag(self):
        self.assertTrue(self.manager.config.features.enable_feature_x)

    def test_cloud_provider(self):
        provider = self.manager.config.cloud_details[self.domain]["provider"]
        self.assertEqual(provider, "aws")

    def test_database_port(self):
        port = self.manager.config.database_details[self.domain]["port"]
        self.assertEqual(port, 5432)

    def test_api_key_validity(self):
        api_key = self.manager.config.cloud_secrets[self.domain]["api_key"]
        self.assertIsInstance(api_key, str)
        self.assertNotEqual(api_key, "REPLACE_ME")
        self.assertGreater(len(api_key), 10)

    def test_domain_in_database_config(self):
        self.assertIn(self.domain, self.manager.config.database_details.to_dict())

    def test_domain_mapping_match(self):
        db_keys = set(self.manager.config.database_details.to_dict().keys())
        cloud_keys = set(self.manager.config.cloud_details.to_dict().keys())
        self.assertEqual(db_keys, cloud_keys)

    def test_secrets_file_exists(self):
        self.assertTrue(self.manager.secrets_path.exists())

if __name__ == "__main__":
    unittest.main()
