from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mus.api.routes import api_router
from mus.core.app_logger.fabrics.config_init import init_logger_from_config


def setup_routers(app, config) -> None:
    app.include_router(api_router, prefix=config["API_V1_STR"])


def setup_middlewares(app, config) -> None:
    # CORS
    origins = []

    # Set all CORS enabled origins: adding security between Backend and Frontend
    if cors_origin := config["BACKEND_CORS_ORIGINS"]:
        origins_raw = cors_origin.split(",")

        for origin in origins_raw:
            use_origin = origin.strip()
            origins.append(use_origin)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),


def create_api() -> FastAPI:
    from mus.api.config.config import api_config

    logger = init_logger_from_config(
        name=api_config["PROJECT_NAME"],
        config=api_config,
    )

    app = FastAPI(
        title=api_config["PROJECT_NAME"],
        version=api_config["APP_VERSION"],
        docs_url=None if api_config["FASTAPI_ENV"] == "prod" else "/docs",
        redoc_url=None if api_config["FASTAPI_ENV"] == "prod" else "/redoc",
        openapi_url=f"{api_config['API_V1_STR']}/openapi.json",
    )

    setup_routers(app, api_config)
    setup_middlewares(app, api_config)

    logger.info("Application API is created")

    return app
