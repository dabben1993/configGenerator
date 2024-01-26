import json
from dataclasses import dataclass, asdict

import yaml


@dataclass
class DbConfig:
    database: dict
    logging: dict

    def to_json(self):
        return json.dumps({"config": asdict(self)}, indent=2)

    def __repr__(self):
        return f"DbConfig(database={self.database}, logging={self.logging})"
