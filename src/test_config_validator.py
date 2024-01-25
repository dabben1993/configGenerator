import unittest
import os
from config_validator import ConfigValidator


class TestConfigValidator(unittest.TestCase):


    def setUp(self):
        self.validator = ConfigValidator(schema_path="../config/cerberus_schema.yml",
                                         file_path="../tests/test.yml",
                                         json_output_path="../tests/output/",
                                         destination="../tests/output/")


    def test_valid_config(self):
        self.validator.validate_yml(self.validator.file_path, self.validator.destination)
        # Add assertions based on your expected valid config
    def test_invalid_config(self):
        file_path = "path/to/invalid/config.yml"
        self.assertTrue(os.path.exists(file_path))
        with self.assertRaises(Exception):
            self.validator.validate_yml(file_path, destination="../tests/ooutput/")
        # Add more assertions based on your expected invalid config

    def test_convert_to_json(self):
        file_path = "path/to/valid/config.yml"
        self.assertTrue(os.path.exists(file_path))
        json_output_path = "path/to/json/output.json"
        self.validator.convert_to_json(file_path, json_output_path)
        # Add more assertions based on your expected JSON output


if __name__ == '__main__':
    unittest.main()
