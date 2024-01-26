import json
import os
import yaml


class FileHandler:
    def __init__(self, source_directory, destination_directory):
        self.source_directory = source_directory
        self.destination_directory = destination_directory

    def read_yaml(self, file_name):
        print(file_name)
        file_path = os.path.join(file_name)
        print(file_path)
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def convert_to_json(self, data):
        return data.to_json() if hasattr(data, 'to_json') else json.dumps(data, indent=2)

    def save_as_json(self, data, output_directory, file_name):
        json_output_path = os.path.join(output_directory, file_name + ".json")
        os.makedirs(output_directory, exist_ok=True)

        with open(json_output_path, 'w') as json_output_file:
            json_output_file.write(data)

        print(f"JSON object written to {json_output_path}")
