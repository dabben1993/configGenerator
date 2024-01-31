import json
import os
import yaml
from structlog import get_logger
from git import Repo

log = get_logger()


def save_as_json(data, file_name, output_directory):
    output_directory = output_directory
    try:
        os.makedirs(output_directory, exist_ok=True)
        json_output_path = os.path.join(output_directory, file_name + ".json")
        with open(json_output_path, 'w') as json_output_file:
            json.dump(data, json_output_file, indent=2)
        log.info("File saved as JSON", data=data, file_path=json_output_path)
    except Exception as e:
        log.error("Error saving JSON file", error=str(e))


def find_file_path(repo_path, file_name):
    try:
        repo = Repo(repo_path)

        for root, dirs, files in os.walk(repo.working_dir):
            if file_name in files:
                file_path = os.path.join(root, file_name)
                log.info("File found", file_path=file_path)
                return file_path

        log.warning("File not found", file_name=file_name)
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def read_yaml(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        log.error("Error reading YAML file", error=str(e))
        return None
