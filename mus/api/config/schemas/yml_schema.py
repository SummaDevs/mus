"""
YML schema

"""

import trafaret as t

from mus.core.app_config.base_config import TrafaretConfigSchemaBase
from mus.core.app_config.config_std import db_credentials_schema
from mus.core.app_config.config_std import logger_schema
from mus.core.text.str_utils import str_strip


class YamlConfigSchema(TrafaretConfigSchemaBase):
    """
    Schema for main (base) config

    """

    def get_validator(self):
        """
        Get validator to validate config schema

        :return: trafaret validator
        :rtype: t.Dict

        """

        return t.Dict({
            t.Key("CONFIG_API") >> "CONFIG_API": t.Dict({

                t.Key("PROJECT_NAME"): str_strip(min_length=3, max_length=64),

                t.Key("API_V1_STR"): str_strip(min_length=3, max_length=64),
                t.Key("APP_VERSION"): str_strip(min_length=3, max_length=64),

                t.Key("FASTAPI_ENV"): str_strip(min_length=3, max_length=64),

                t.Key("UVICORN_HOST"): str_strip(min_length=3, max_length=64),
                t.Key("UVICORN_PORT"): t.Int(gte=64, lte=65000),
                t.Key("BACKEND_CORS_ORIGINS", optional=True): str_strip(
                    min_length=1, max_length=255),

                t.Key("DATE_FORMAT"): str_strip(min_length=8, max_length=10),

                t.Key("DB", optional=True): db_credentials_schema(prefix=""),

                t.Key("LOGGER", optional=True): logger_schema(prefix=""),

                t.Key("DATA_PROCESSING"): t.Dict({
                    t.Key("INPUT_FOLDER"): str_strip(
                        min_length=5, max_length=64),
                    t.Key("OUTPUT_FOLDER"): str_strip(
                        min_length=5, max_length=64),
                }),

            })
        })
