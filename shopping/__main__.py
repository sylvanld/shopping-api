from click import Group as CliGroup

from shopping.api.factory import create_api
from shopping.core.config import EnvironmentConfig
from shopping.core.extensions import ExtensionsManager
from shopping.core.logging import setup_logging
from shopping.extensions.database import DatabaseExtension

cli = CliGroup()
config = EnvironmentConfig()

setup_logging(config)

api = create_api(config)

extensions = ExtensionsManager(api, cli, config)
extensions.register(DatabaseExtension)


if __name__ == "__main__":
    cli()
