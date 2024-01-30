import unittest
from unittest.mock import patch, MagicMock
from src.config_validator import ConfigValidator


class TestConfigValidator(unittest.TestCase):
    def setUp(self):
        # Set up common variables for tests
        self.schema_path = "test_cerberus_schema.yml"
        self.file_path = "test.yml"
        self.json_output_path = "output"
        self.destination = "output"
        self.validator = MagicMock()
        self.file_handler = MagicMock()
        self.config_validator = ConfigValidator(
            self.schema_path,
            self.file_path,
            self.json_output_path,
            self.destination
        )

    @patch("config_validator.ConfigValidator")
    def test_valid_configuration(self, mock_file_helper):
        # Test case: Valid configuration
        mock_file_helper.return_value.read_yaml.return_value = {"config": {"key": "value"}}
        self.validator.validate.return_value = True

        with patch("config_validator.DbConfig") as mock_db_config:
            result = self.config_validator.process_configuration()

        mock_db_config.assert_called_once_with(key="value")
        self.file_handler.save_as_json.assert_called_with(
            data=mock_db_config.return_value.to_json(),
            file_name="config"
        )
        self.assertEqual(result, None)

    @patch("config_validator.FileHelper")
    def test_missing_config_data(self, mock_file_helper):
        # Test case: Missing config data
        mock_file_helper.return_value.read_yaml.return_value = None
        result = self.config_validator.process_configuration()
        self.assertEqual(result, None)

    @patch("config_validator.FileHelper")
    def test_invalid_configuration(self, mock_file_helper):
        # Test case: Invalid configuration
        mock_file_helper.return_value.read_yaml.return_value = {"config": {"key": "value"}}
        self.validator.validate.return_value = False
        result = self.config_validator.process_configuration()
        self.assertEqual(result, None)

    # Add more test cases as needed


if __name__ == "__main__":
    unittest.main()
