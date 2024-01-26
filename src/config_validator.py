import os
import json

import cerberus
import yaml
from db_config import DbConfig


class ConfigValidator:
    def __init__(self, schema_path, file_path, json_output_path=None, destination=None):
        self.json_output_path = json_output_path
        self.schema_path = schema_path
        self.file_path = file_path
        self.json_output_path = json_output_path
        self.destination = destination
        self.validator = self.load_schema()
        self.process_configuration()

    def load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            return cerberus.Validator(schema)

    def process_configuration(self):
        config_data = self.read_config_file()
        if config_data:
            db_config = self.create_db_config(config_data)
            self.save_as_json(db_config)
            self.convert_to_json_file()

    def read_config_file(self):
        with open(self.file_path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def create_db_config(self, config_data):
        if self.validator.validate(config_data):
            print("Configuration is valid.")
            return DbConfig(**config_data.get('config', {}))
        else:
            print("Invalid configuration:")
            for error in self.validator.errors:
                print(f"  - {error}: {self.validator.errors[error]}")
            return None

    def save_as_json(self, db_config):
        json_output_path = os.path.join(self.destination, "db_config.json")
        os.makedirs(self.destination, exist_ok=True)

        with open(json_output_path, 'w') as json_output_file:
            json_output_file.write(db_config.to_json())

        print(f"DbConfig object written to {json_output_path}")

    def convert_to_json_file(self):
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]

        # Construct the JSON output path by combining the destination and file name
        json_output_path = os.path.join(self.destination, file_name + ".json")

        with open(self.file_path, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)

        json_output = json.dumps(config_data, indent=2)

        with open(json_output_path, 'w') as json_output_file:
            json_output_file.write(json_output)

        print(f"JSON object written to {json_output_path}")