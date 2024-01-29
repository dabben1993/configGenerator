import os
import unittest
from io import StringIO
from unittest.mock import mock_open, patch
from src.file_helper import FileHelper


class TestFileHelper(unittest.TestCase):
    def setUp(self):
        self.file_path = "test.yml"
        self.destination = "output"

    @patch("src.file_helper.os.makedirs")
    @patch("builtins.open", new_callable=mock_open())
    def test_read_yaml(self, mock_open, mock_makedirs):
        # Prepare a fake YAML content
        yaml_content = "key: value"

        # Mock the open function to return the fake content
        with patch("src.file_helper.open", new_callable=mock_open()) as mock_open:
            mock_open.return_value = StringIO(yaml_content)

            # Create FileHandler instance
            file_helper = FileHelper(self.file_path, self.destination)

            # Call the read_yaml method
            result = file_helper.read_yaml()

            # Assert that the open function was called with the correct file path
            mock_open.assert_called_once_with(self.file_path, 'r')

            # Assert that the result matches the expected YAML content
            self.assertEqual(result, {"key": "value"})

    @patch("src.file_helper.os.makedirs")
    @patch("builtins.open", new_callable=mock_open())
    def test_read_yaml_exception(self, mock_open, mock_makedirs):
        # Create FileHandler instance
        file_helper = FileHelper(self.file_path, self.destination)

        # Mock an exception when trying to read YAML
        mock_open.side_effect = Exception("An error occurred")

        # Call the read_yaml method
        result = file_helper.read_yaml()

        # Assert that the open function was called with the correct file path
        mock_open.assert_called_once_with(self.file_path, 'r')

        # Ensure the result is None when an exception occurs
        self.assertIsNone(result)

    @patch("src.file_helper.os.makedirs")
    @patch("builtins.open", new_callable=mock_open())
    def test_save_as_json(self, mock_open, mock_makedirs):
        # Prepare data to be saved as JSON
        data = {"key": "value"}
        file_name = "output_file"

        # Create FileHandler instance
        file_helper = FileHelper(self.file_path, self.destination)

        # Call the save_as_json method
        file_helper.save_as_json(data, file_name)

        # Assert that the makedirs function was called with the correct directory
        mock_makedirs.assert_called_once_with(self.destination, exist_ok=True)

        # Assert that the open function was called with the correct file path
        json_output_path = os.path.join(self.destination, file_name + ".json")
        mock_open.assert_called_once_with(json_output_path, 'w')

    @patch("src.file_helper.os.makedirs")
    @patch("builtins.open", new_callable=mock_open())
    def test_save_as_json_exception(self, mock_open, mock_makedirs):
        # Prepare data to be saved as JSON
        data = {"key": "value"}
        file_name = "output_file"

        # Create FileHandler instance
        file_helper = FileHelper(self.file_path, self.destination)

        # Mock an exception when trying to save as JSON
        mock_open.side_effect = Exception("An error occurred")

        # Call the save_as_json method
        file_helper.save_as_json(data, file_name)

        # Assert that the makedirs function was called with the correct directory
        mock_makedirs.assert_called_once_with(self.destination, exist_ok=True)

        # Assert that the open function was called with the correct file path
        json_output_path = os.path.join(self.destination, file_name + ".json")
        mock_open.assert_called_once_with(json_output_path, 'w')


if __name__ == "__main__":
    unittest.main()
