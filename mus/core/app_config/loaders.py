import json
import os
from importlib.machinery import SourceFileLoader

import yaml
from dotenv import dotenv_values

from .abstracts import AbstractLoader


class ObjectLoader(AbstractLoader):
    """
    Loader to load app_config data from python module

    """

    @classmethod
    def load(cls, obj):
        """
        Load data from python object

        :param obj: python obj
        :type obj: any

        :return: app_config data
        :rtype: dict

        """

        return dict(
            (param_name, getattr(obj, param_name))
            for param_name in filter(str.isupper, dir(obj))
        )


class ModuleLoader(AbstractLoader):
    """
    Loader to load app_config data from python module

    """

    @classmethod
    def load(cls, module_path):
        """
        Load app_config data from python module use module path

        :param module_path: module path
        :type module_path: str

        :return: app_config data
        :rtype: dict

        """

        path, module_name = os.path.split(module_path)

        if path:
            module_ = SourceFileLoader(module_name.replace(".py", ""),
                                       module_path)
        elif module_name.endswith(".py"):
            module_ = __import__(module_name.replace(".py", ""))
        else:
            module_ = __import__(module_name)

        module = module_.load_module() if hasattr(module_,
                                                  "load_module") else module_

        return ObjectLoader.load(obj=module)


class ENVLoader(AbstractLoader):
    """
    Loader to load app_config data from environment

    """

    @classmethod
    def load(cls):
        """
        Load app_config data from environment

        :return: app_config data
        :rtype: dict

        """

        return dict(os.environ)


class DotENVLoader(AbstractLoader):
    """
    Loader to load app_config data from .venv file

    """

    @classmethod
    def load(cls, file_path):
        """
        Load app_config data from .env file

        :return: app_config data
        :rtype: dict

        """

        dotenv_values(file_path)


class YamlLoader(AbstractLoader):
    """
    Loader to load app_config data from yaml file

    """

    @classmethod
    def load(cls, file_path):
        """
        Load app_config data from YAML file

        :return: app_config data
        :rtype: dict

        """

        # load base data
        with open(file_path, "r") as open_file:
            return yaml.load(open_file, Loader=yaml.SafeLoader)


class JSONLoader(AbstractLoader):
    """
    Loader to load app_config data from json file

    """

    @classmethod
    def load(cls, file_path):
        """
        Load app_config data from JSON file

        :return: app_config data
        :rtype: dict

        """

        with open(file_path, "r") as open_file:
            return json.load(open_file)
