"""Application module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .containers import Application
from .settings import Settings
from .endpoints import api


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]


def create_app() -> FastAPI:
    """Failurebase app factory."""

    container = Application()
    container.config.from_pydantic(Settings())

    db = container.adapters.db()
    db.create_database()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.container = container
    app.include_router(api.router)

    return app


app = create_app()
