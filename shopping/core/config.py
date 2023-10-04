import os
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T")
UNDEFINED = ...


def nest_flat_structure(d: Dict[str, Any], out: dict = None):
    if out is None:
        out = {}

    for key, value in d.items():
        if "." in key:
            top_level_key, nested_keys = key.split(".", maxsplit=1)
            if out.get(top_level_key, UNDEFINED) is UNDEFINED:
                out[top_level_key] = {}
            nest_flat_structure({nested_keys: value}, out[top_level_key])
        else:
            out[key] = value

    return out


class Config:
    def __init__(self):
        self.__cache = {}

    def dump(self):
        """Dump config loader cache for debugging."""
        return nest_flat_structure(self.__cache)

    def get_raw(self, key: str, default) -> str:
        """Load raw config value as a string"""
        raise NotImplementedError

    def get(self, key: str, default=UNDEFINED, type: Type[T] = str) -> T:
        """Generic method that return typed value for a config option.

        If option has already been loaded, returns value from cache.
        """
        cached_value = self.__cache.get(key, UNDEFINED)
        if cached_value != UNDEFINED:
            return cached_value

        raw_value = self.get_raw(key, default)

        if raw_value is UNDEFINED:
            return UNDEFINED

        if type is str:
            value = str(raw_value)
        elif type is bool:
            if raw_value in ("1", "true", "True", "yes"):
                value = True
            elif raw_value in ("0", "false", "False", "no"):
                value = False
            else:
                raise ValueError("Unsupported format for boolean: %s=%s" % (key, raw_value))
        else:
            raise ValueError("Unsupported type for config key: type=%s" % type)

        self.__cache[key] = value
        return value


class EnvironmentConfig(Config):
    def get_raw(self, key: str, default) -> str:
        envvar = key.replace(".", "_").upper()
        return os.getenv(envvar, default)
