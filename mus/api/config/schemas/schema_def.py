import trafaret as t
from trafaret.keys import subdict

from mus.core.app_config.config_std import db_credentials_schema
from mus.core.app_config.config_std import logger_schema
from mus.core.text.str_utils import str_strip

api_config_def = t.Dict(

    subdict(
        "CONFIG_API",
        t.Key(
            name="FASTAPI_ENV",
            optional=True,
            trafaret=str_strip(
                nullable=True, min_length=3, max_length=64)
        ),
        t.Key(
            name="UVICORN_HOST",
            optional=True,
            trafaret=str_strip(
                nullable=True, min_length=4, max_length=64)
        ),
        t.Key(
            name="UVICORN_PORT",
            optional=True,
            trafaret=t.Int(gte=64, lte=65000)
        ),

        t.Key(
            name="BACKEND_CORS_ORIGINS",
            optional=True,
            trafaret=str_strip(
                nullable=True, min_length=4, max_length=64)
        ),

        subdict(
            "DB",
            *db_credentials_schema(prefix="").keys,
            trafaret=lambda x: x
        ),

        subdict(
            "LOGGER",
            *logger_schema(prefix="").keys,
            trafaret=lambda x: x
        ),

        trafaret=lambda x: x
    ),

    ignore_extra="*"
)
