import os


class Config:
    def get(self, key: str) -> str:
        ...


class EnvironmentConfig(Config):
    def get(self, key: str, default) -> str:
        envvar = key.replace(".", "_").upper()
        return os.getenv(envvar, default)
