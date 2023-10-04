import logging
from dataclasses import dataclass
from typing import Any, List, Type

from click import Group as CliGroup
from fastapi import FastAPI

from shopping.core.config import Config

UNDEFINED = ...
LOG = logging.getLogger(__name__)


class ConfigurationError(Exception):
    ...


@dataclass
class ExtensionOption:
    key: str
    description: str
    required: bool = True
    type: Type = str
    default: Any = UNDEFINED

    def __post_init__(self):
        if self.default is not UNDEFINED:
            self.required = False


class Extension:
    name: str = None
    options: List[ExtensionOption] = None

    def configure(self, config: Config):
        if self.options is None:
            return

        self.config = {}
        for option in self.options:
            value = config.get(option.key, UNDEFINED, type=option.type)
            if value is UNDEFINED:
                if option.required:
                    raise ConfigurationError(option.key)
                value = None if option.default is UNDEFINED else option.default
            self.config[option.key] = value
            LOG.debug("Loading config option %s=%s", option.key, value)

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
        LOG.info("Registering extension %s", extension_cls.name)
        extension = extension_cls()
        extension.configure(self.config)
        extension.initialize()
        extension.register(self.api, self.cli)
