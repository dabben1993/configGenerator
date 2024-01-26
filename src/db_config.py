import json

import yaml


class DbConfig:
    def __init__(self, database=None, logging=None):
        self.database = database or {}
        self.logging = logging or {}

    def to_json(self):
        return json.dumps({"config": {"database": self.database, "logging": self.logging}}, indent=2)

    def __repr__(self):
        return f"DbConfig(database={self.database}, logging={self.logging})"
