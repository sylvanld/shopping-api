from fastapi import FastAPI

from shopping.api.metadata import API_DESCRIPTION, API_TITLE, API_VERSION


def create_api():
    api = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        docs_url="/",
    )
    return api
