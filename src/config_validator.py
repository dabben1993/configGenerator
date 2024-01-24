import cerberus
import yaml

class ConfigValidator:
    def __init__(self):
        self.schema_path = "../config/cerberus_schema.yml"
        self.validator = self._load_schema()

    def _load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
            return cerberus.Validator(schema)

    def validate_yml(self, file_path):
        with open(file_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)

        if self.validator.validate(config_data):
            print("Configuration is valid.")
        else:
            print("Invalid configuration:")
            for error in self.validator.errors:
                print(f"  - {error}: {self.validator.errors[error]}")
