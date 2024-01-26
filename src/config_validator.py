import os
import json

import cerberus
import yaml
from db_config import DbConfig
from file_helper import FileHandler


class ConfigValidator:
    def __init__(self, schema_path, file_path, json_output_path=None, destination=None):
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
        file_handler = FileHandler(self.file_path, self.destination)
        config_data = file_handler.read_yaml(self.file_path)
        if config_data:
            db_config = self.create_db_config(config_data)
            file_handler.save_as_json(data=file_handler.convert_to_json(db_config), file_name=os.path.splitext(os.path.basename(self.file_path))[0],
                                      output_directory=self.destination)
            file_handler.save_as_json(data=file_handler.convert_to_json(db_config), file_name="db_config", output_directory=self.destination)


    def create_db_config(self, config_data):
        if self.validator.validate(config_data):
            print("Configuration is valid.")
            return DbConfig(**config_data.get('config', {}))
        else:
            print("Invalid configuration:")
            for error in self.validator.errors:
                print(f"  - {error}: {self.validator.errors[error]}")
            return None
