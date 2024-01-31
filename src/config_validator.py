import json
import os
from dataclasses import asdict

from structlog import get_logger
import cerberus
import yaml
from db_config import DbConfig
import file_helper

log = get_logger()


class ConfigValidator:

    def __init__(self, schema_path, repo_path, json_output_path=None, destination=None, file_name=None):
        self.schema_path = schema_path
        self.repo_path = repo_path
        self.json_output_path = json_output_path
        self.destination = destination
        self.file_name = file_name
        self.validator = self.load_schema()
        self.process_configuration()

    def load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            log.info("Schema loaded", schema=schema)
            return cerberus.Validator(schema)

    def process_configuration(self):
        config_data = file_helper.read_yaml(file_helper.find_file_path(self.repo_path, self.file_name))
        if config_data:
            log.info("Config data exists", config_data=config_data)
            db_config = self.create_db_config(config_data)
            if db_config:
                log.info("db_config object created", object=db_config)
                file_helper.save_as_json(data=json.dumps({"config": asdict(db_config)}, indent=2),
                             file_name=os.path.splitext(os.path.basename(self.repo_path))[0],
                             output_directory=self.destination)
                log.info("File saved")

                file_helper.save_as_json(data=json.dumps({"config": asdict(db_config)}, indent=2),
                                         file_name="db_config", output_directory=self.destination)
                log.info("File saved")

    def create_db_config(self, config_data):
        if self.validator.validate(config_data):
            log.info("Configuration is valid.", configuration=DbConfig(**config_data.get('config', {})))
            return DbConfig(**config_data.get('config', {}))
        else:
            for error in self.validator.errors:
                log.warning("Invalid configuration:", f"  - {error}: {self.validator.errors[error]}")
            return None
