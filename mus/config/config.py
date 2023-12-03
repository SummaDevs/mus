import os

from mus.core.app_config.base_factory import BaseConfigFactory
from mus.core.app_config.config_obj import ConfigObj
from .schemas.dotenv_schema import DotEnvConfigSchema
from .schemas.env_schema import EnvConfigSchema
from .schemas.yml_schema import YamlConfigSchema

yml_config_file = os.path.join("mus", "config", "config.yaml")


class YamlConfigFactory(BaseConfigFactory):
    schema = YamlConfigSchema


class DotEnvConfigFactory(BaseConfigFactory):
    schema = DotEnvConfigSchema


class EnvConfigFactory(BaseConfigFactory):
    schema = EnvConfigSchema


config_obj = ConfigObj(EnvConfigFactory, DotEnvConfigFactory, YamlConfigFactory)

app_config = config_obj(yml_config_file, "CONFIG_DATA")
