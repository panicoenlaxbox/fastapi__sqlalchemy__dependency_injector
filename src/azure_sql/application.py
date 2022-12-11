from fastapi import FastAPI

import azure_sql.routers.debug
import azure_sql.routers.subscriptions
from azure_sql.containers import Container
from azure_sql.handlers import mediator


def create_app() -> FastAPI:
    container = Container()
    container.override_providers(mediator=mediator)
    container.wire(modules=[".handlers"], packages=[".routers"])
    app_ = FastAPI()
    app_.container = container  # type: ignore[attr-defined]
    app_.include_router(azure_sql.routers.subscriptions.router)
    app_.include_router(azure_sql.routers.debug.router)
    return app_


app = create_app()
