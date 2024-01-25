import json
import os

import cerberus
import yaml


class ConfigValidator:
    def __init__(self, schema_path, file_path, json_output_path=None):
        self.schema_path = schema_path
        file_path = file_path
        json_output_path = json_output_path
        self.validator = self._load_schema()

        self._validate_yml(file_path)
        self._convert_to_json(file_path, json_output_path)

    def _load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            return cerberus.Validator(schema)

    def _validate_yml(self, file_path):
        with open(file_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)

        if self.validator.validate(config_data):
            print("Configuration is valid.")
        else:
            print("Invalid configuration:")
            for error in self.validator.errors:
                print(f"  - {error}: {self.validator.errors[error]}")

    def _convert_to_json(self, file_path, json_output_path=None):
        with open(file_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)

        json_output = json.dumps(config_data, indent=2)

        if json_output_path:
            output_directory = os.path.dirname(json_output_path)
            os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

            with open(json_output_path, 'w') as json_output_file:
                json_output_file.write(json_output)
            print(f"JSON object written to {json_output_path}")
        else:
            print("JSON object:")
            print(json_output)
