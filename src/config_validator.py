import json
import os

import cerberus
import yaml

class AppConfig:
    def __init__(self, database=None, logging=None):
        self.database = database or {}
        self.logging = logging or {}

    def to_json(self):
        return json.dumps(self.__dict__, indent=2)

    def __repr__(self):
        return f"AppConfig(database={self.database}, logging={self.logging})"


class ConfigValidator:
    def __init__(self, schema_path, file_path, json_output_path=None, destination=None):
        self.schema_path = schema_path
        file_path = file_path
        json_output_path = json_output_path
        destination = destination
        self.validator = self.load_schema()

        self.validate_yml(file_path, destination)
        self.convert_to_json(file_path, json_output_path)

    def load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            return cerberus.Validator(schema)

    def validate_yml(self, file_path, destination):
        with open(file_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)

        if self.validator.validate(config_data):
            print("Configuration is valid")
            app_config = AppConfig(**config_data.get('config', {}))
            print("AppConfig object:", app_config)

            # Save AppConfig as JSON
            json_output_path = os.path.join(destination, "app_config.json")
            os.makedirs(destination, exist_ok=True)
            with open(json_output_path, 'w') as json_output_file:
                json_output_file.write(app_config.to_json())
            print(f"AppConfig object written to {json_output_path}")
        else:
            print("Invalid configuration:")
            for error in self.validator.errors:
                print(f"  - {error}: {self.validator.errors[error]}")

    def convert_to_json(self, file_path, json_output_path=None):
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
