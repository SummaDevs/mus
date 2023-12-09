import os
import pathlib

from mus.constant.constant import BASE_DIR
from mus.core.container.dict_utils import dict_deep_update


class ConfigObj:
    config = None

    def __init__(self, env_factory, dot_env_factory, yaml_factory):
        self.env_factory = env_factory
        self.dot_env_factory = dot_env_factory
        self.yaml_factory = yaml_factory

    def get_config(self, yml_config_path=None, section=None):
        """
        Config precedence: yml <- .env <- env vars (if not None)
        """

        # get configs
        env_config = self.env_factory.get_config_from_env()

        dot_env_path = os.path.join(BASE_DIR, ".env")
        dot_env_config = self.dot_env_factory.get_config_from_dotenv(
            file_path=dot_env_path) if pathlib.Path(dot_env_path).is_file() else {}

        yml_config = self.yaml_factory.get_config_from_yaml(
            file_path=os.path.join(BASE_DIR, yml_config_path)) if yml_config_path else {}

        config = dict_deep_update(yml_config, dot_env_config)
        config = dict_deep_update(config, env_config)

        if section:
            return config[section]

        return config

    def __call__(self, yml_config_path, section, *args, **kwargs):
        if self.config:
            return self.config

        self.config = self.get_config(yml_config_path, section)

        return self.config
