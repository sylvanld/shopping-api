from click import Group as CliGroup

from shopping.api.factory import create_api
from shopping.core.config import EnvironmentConfig
from shopping.core.extensions import ExtensionsManager
from shopping.extensions.database import DatabaseExtension

api = create_api()
cli = CliGroup()
config = EnvironmentConfig()


extensions = ExtensionsManager(api, cli, config)
extensions.register(DatabaseExtension)


if __name__ == "__main__":
    cli()
