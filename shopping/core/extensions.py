from dataclasses import dataclass
from typing import Any, List, Type

from click import Group as CliGroup
from fastapi import FastAPI

from shopping.core.config import Config

UNDEFINED = ...


class ConfigurationError(Exception):
    ...


@dataclass
class ExtensionOption:
    key: str
    description: str
    required: bool = True
    default: Any = UNDEFINED

    def __post_init__(self):
        if self.default is not UNDEFINED:
            self.required = False


class Extension:
    options: List[ExtensionOption] = None

    def configure(self, config: Config):
        if self.options is None:
            return

        self.config = {}
        for option in self.options:
            value = config.get(option.key, UNDEFINED)
            if value is UNDEFINED:
                if option.required:
                    raise ConfigurationError(option.key)
                value = None if option.default is UNDEFINED else option.default
            self.config[option.key] = value

    def initialize(self):
        ...

    def register(self, api: FastAPI, cli: CliGroup):
        ...


class ExtensionsManager:
    def __init__(self, api: FastAPI, cli: CliGroup, config: Config):
        self.api = api
        self.cli = cli
        self.config = config

    def register(self, extension_cls: Type[Extension]):
        print("registering extension", extension_cls)
        extension = extension_cls()
        print("configuring extension", extension_cls)
        extension.configure(self.config)
        print("initializing extension", extension_cls)
        extension.initialize()
        print("registering extension addons", extension_cls)
        extension.register(self.api, self.cli)
