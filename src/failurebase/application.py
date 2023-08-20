"""Application module."""

import logging
import logging.config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from failurebase.containers import Application
from failurebase.settings import Settings
from failurebase.endpoints import api


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Failurebase app factory."""

    container = Application()
    container.config.from_pydantic(Settings())

    logging.config.fileConfig(container.config.LOGGING_CONFIGURATION_FILE(), disable_existing_loggers=False)
    logger.info('Failurebase starting...')

    db = container.adapters.db()
    db.create_database()

    app = FastAPI(docs_url=None)
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
        logger.info('CORS enabled. Allowed origins: %s', allow_origins)

    if container.config.CLIENT_FROM_APP():

        templates = Jinja2Templates(directory=container.config.RESOURCES_DIR() / 'frontend')

        app.mount('/static',
                  StaticFiles(directory=container.config.RESOURCES_DIR() / 'frontend' / 'static', html=True),
                  name='static')

        app.include_router(api.router)

        @app.get("/{rest_of_path:path}")
        def react_app(req: Request, rest_of_path: str):
            return templates.TemplateResponse('index.html', {'request': req, 'api_url': 'http://localhost:8000'})

        logger.info('Frontend client and API are served from failurebase web app')

    else:

        app.include_router(api.router)

        logger.info('Only API is served from failurebase web app')

    return app
