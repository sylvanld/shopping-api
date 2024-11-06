import logging

from click import Group as CliGroup
from click import group as cli_group
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware

from shopping.core.extensions import Extension, ExtensionOption

LOG = logging.getLogger(__name__)
session = scoped_session(session_factory=sessionmaker())


@cli_group("database")
def db_cli():
    """Commands to manage app database"""


class Entity(DeclarativeBase):
    ...


class Repository:
    session: Session

    def __init__(self):
        self.session = session

    def add(self, entity):
        self.session.add(entity)

    def commit(self):
        self.session.commit()

    def delete(self, entity):
        self.session.delete(entity)


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        session.rollback()
        return response


class DatabaseExtension(Extension):
    name = "database"
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
        self.engine = create_engine(database_url)
        session.bind = self.engine
        if self.config.get("database.auto_migrate"):
            Entity.metadata.create_all(self.engine)

    def register(self, api: FastAPI, cli: CliGroup):
        api.add_middleware(DatabaseMiddleware)
        cli.add_command(db_cli)
