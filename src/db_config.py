import yaml

class DbConfig:
    def __init__(self, config=None):
        self.config = config or {}

    @classmethod
    def from_yml_file(cls, file_path):
        with open(file_path, 'r') as yml_file:
            yml_data = yaml.safe_load(yml_file)
            return cls(config=yml_data.get('config', {}))

    def __repr__(self):
        return f"DbConfig(config={self.config})"
