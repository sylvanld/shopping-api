import logging

from click import Group as CliGroup
from click import group as cli_group
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from shopping.core.extensions import Extension, ExtensionOption

LOG = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s :: %(asctime)s :: %(message)s", level=logging.DEBUG)
session = scoped_session(session_factory=sessionmaker())
print("tadata")
LOG.info("doudou")


@cli_group("database")
def db_cli():
    """Commands to manage app database"""


class Entity(DeclarativeBase):
    ...


class DatabaseExtension(Extension):
    options = [
        ExtensionOption(
            key="database.url",
            description=(
                "URL connection database following RFC-1738." "(dialect+driver://username:password@host:port/database)"
            ),
            default="sqlite:///:memory:",
        ),
        ExtensionOption(
            key="database.auto_migrate",
            description=("Whether all schemas should be created skipping database migrations"),
            default=True,
        ),
    ]

    def initialize(self):
        database_url = self.config.get("database.url")
        print("database url", database_url)
        LOG.info("Initializing database engine with URL: %s", database_url)
        self.engine = create_engine(database_url)
        session.bind = self.engine
        if self.config.get("database.auto_migrate"):
            Entity.metadata.create_all(self.engine)

    def register(self, api: FastAPI, cli: CliGroup):
        cli.add_command(db_cli)
