"""
environmental variables config

"""

import trafaret as t

from mus.core.app_config.base_config import TrafaretConfigSchemaBase
from .schema_def import api_config_def


class DotEnvConfigSchema(TrafaretConfigSchemaBase):
    """
    Schema for env (secret) config

    """

    def get_validator(self):
        """
        Get validator to validate config schema

        :return: trafaret validator
        :rtype: t.Dict

        """

        return api_config_def
