from fastapi import FastAPI

import shopping.api.v1.carts
import shopping.api.v1.items
from shopping.api.metadata import API_DESCRIPTION, API_TAGS, API_TITLE, API_VERSION


def create_api():
    api = FastAPI(
        title=API_TITLE, version=API_VERSION, description=API_DESCRIPTION, openapi_tags=API_TAGS, docs_url="/"
    )

    api.include_router(shopping.api.v1.carts.router, prefix="/v1")
    api.include_router(shopping.api.v1.items.router, prefix="/v1")

    return api
