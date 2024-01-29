import os
from structlog import get_logger
import cerberus
import yaml
from db_config import DbConfig
from file_helper import FileHelper

log = get_logger()


class ConfigValidator:

    def __init__(self, schema_path, file_path, json_output_path=None, destination=None):
        self.schema_path = schema_path
        self.file_path = file_path
        self.json_output_path = json_output_path
        self.destination = destination
        self.validator = self.load_schema()
        self.file_handler = FileHelper(self.file_path, self.destination)
        self.process_configuration()

    def load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            log.info("Schema loaded", schema=schema)
            return cerberus.Validator(schema)

    def process_configuration(self):
        config_data = self.file_handler.read_yaml()
        if config_data:
            log.info("Config data exists", config_data=config_data)
            db_config = self.create_db_config(config_data)
            if db_config:
                log.info("db_config object created", object=db_config)
                self.file_handler.save_as_json(data=db_config.to_json(),
                                               file_name=os.path.splitext(os.path.basename(self.file_path))[0])
                log.info("File saved")

                self.file_handler.save_as_json(data=db_config.to_json(), file_name="db_config")
                log.info("File saved")

    def create_db_config(self, config_data):
        if self.validator.validate(config_data):
            log.info("Configuration is valid.", configuration=DbConfig(**config_data.get('config', {})))
            return DbConfig(**config_data.get('config', {}))
        else:
            for error in self.validator.errors:
                log.warning("Invalid configuration:", f"  - {error}: {self.validator.errors[error]}")
            return None
