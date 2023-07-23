"""Application module."""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .containers import Application
from .settings import Settings
from .endpoints import api


def create_app() -> FastAPI:
    """Failurebase app factory."""

    container = Application()
    container.config.from_pydantic(Settings())

    db = container.adapters.db()
    db.create_database()

    app = FastAPI()
    app.container = container

    allow_origins = container.config.CORS_ALLOWED_ORIGINS()

    if allow_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

    if container.config.CLIENT_FROM_APP():

        templates = Jinja2Templates(directory=container.config.RESOURCES_DIR())

        app.mount('/static',
                  StaticFiles(directory=container.config.RESOURCES_DIR() / 'static', html=True), name='static')

        app.include_router(api.router)

        @app.get("/{rest_of_path:path}")
        def react_app(req: Request, rest_of_path: str):
            return templates.TemplateResponse('index.html', {'request': req, 'api_url': 'http://localhost:8000'})

    else:

        app.include_router(api.router)

    return app
