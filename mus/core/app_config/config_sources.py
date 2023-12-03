import json
import os

import jmespath
import yaml
from dotenv import dotenv_values

from .base_config import BaseConfig


class EnvConfig(BaseConfig):
    """
    Environment variables based config.

    """

    def load(self):
        """
        Load config data
        from environment variables.

        :return: Raw loaded data
        :rtype: dict[Any]

        """
        return dict(os.environ)


class DotEnvConfig(BaseConfig):
    """
    .env based config.

    The syntax of .env files supported by dotenv is similar to that of Bash
    """

    def __init__(self, file_path, schema=None, **kwargs):
        self._file_path = file_path
        super().__init__(schema, **kwargs)

    def load(self):
        """
        Load config data from .env file and doesn't touch the environment

        :return: Raw loaded data
        :rtype: dict[Any]

        """

        return dotenv_values(self._file_path)


class JsonConfig(BaseConfig):
    """
    JSON file based config.

    """

    def __init__(self, file_path, schema=None, sub_path=None, **kwargs):
        self._file_path = file_path
        self._sub_path = sub_path
        super().__init__(schema, **kwargs)

    def load(self):
        """
        Load config data
        from JSON file.

        Load only from sub path is defined.

        :return: Raw loaded data
        :rtype: dict[Any]

        """
        with open(self._file_path, "r") as open_file:
            data = json.load(open_file)

        if self._sub_path:
            return jmespath.search(self._sub_path, data)

        return data


class YamlConfig(BaseConfig):
    """
    YAML file based config.

    """

    def __init__(self, file_path, schema=None, sub_path=None, **kwargs):
        self._file_path = file_path
        self._sub_path = sub_path
        super().__init__(schema, **kwargs)

    def load(self):
        """
        Load config data
        from YAML file.

        Load only from sub path is defined.

        :return: Raw loaded data
        :rtype: dict[Any]

        """
        with open(self._file_path, "r") as open_file:
            data = yaml.load(open_file, Loader=yaml.SafeLoader)

        if self._sub_path:
            return jmespath.search(self._sub_path, data)

        return data
