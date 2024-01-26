import json
import os
import yaml
import structlog

log = structlog.get_logger()


class FileHandler:
    def __init__(self, source_directory, destination_directory):
        self.source_directory = source_directory
        self.destination_directory = destination_directory

    def read_yaml(self, file_name):
        with open(file_name, 'r') as file:
            log.info("File opened", file=file_name + " opened")
            return yaml.safe_load(file)

    def convert_to_json(self, data):
        log.info("File to be converted", org_file=data)
        json_data = data.to_json()
        log.info("File converted to json", json_output=json_data)
        return json_data

    def save_as_json(self, data, output_directory, file_name):
        json_output_path = os.path.join(output_directory, file_name + ".json")
        os.makedirs(output_directory, exist_ok=True)

        with open(json_output_path, 'w') as json_output_file:
            json_output_file.write(data)

        log.info("JSON object created", path=json_output_path)
