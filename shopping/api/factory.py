from fastapi import FastAPI


def create_api():
    api = FastAPI(
        title="Shopping API", description="API that expose features to collaborate on shopping lists.", docs_url="/"
    )
    return api
