from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str


@dataclass
class LoggingConfig:
    level: str
    file_path: str


@dataclass
class DbConfig:
    database: DatabaseConfig
    logging: LoggingConfig

    def __repr__(self):
        return f"DbConfig(database={self.database}, logging={self.logging})"
