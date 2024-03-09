from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import shopping.api.healthcheck
import shopping.api.v1.carts
import shopping.api.v1.items
from shopping.api.metadata import API_DESCRIPTION, API_TAGS, API_TITLE, API_VERSION
from shopping.core.config import Config


def create_api(config: Config):
    api = FastAPI(
        title=API_TITLE, version=API_VERSION, description=API_DESCRIPTION, openapi_tags=API_TAGS, docs_url="/"
    )
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.exception_handler(Exception)
    async def handle_unhandled_exception(request, exc):
        is_debug_mode = config.get("debug", type=bool)
        if is_debug_mode:
            import traceback

            return JSONResponse({"error": str(exc), "traceback": traceback.format_exc().split("\n")}, status_code=401)

    api.include_router(shopping.api.healthcheck.router)
    api.include_router(shopping.api.v1.carts.router, prefix="/v1")
    api.include_router(shopping.api.v1.items.router, prefix="/v1")

    return api
