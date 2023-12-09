import ntpath

import jmespath
import jmespath.exceptions

from .abstracts import AbstractValidator
from .abstracts import EmptyValidator
from .loaders import DotENVLoader
from .loaders import ENVLoader
from .loaders import JSONLoader
from .loaders import ModuleLoader
from .loaders import ObjectLoader
from .loaders import YamlLoader


class ConfigException(BaseException):
    """
    Main exception for all app_config exceptions

    """


class UnknownParameter(ConfigException):
    """
    Can't find expect parameter error

    """


class FileNotFoundException(ConfigException):
    """
    Can't find file use path

    """


class Config(dict):
    """
    Config class

    """

    def __init__(self, *args, defaults=None):
        defaults = args[1] if args else (defaults or {})
        super(Config, self).__init__(defaults or {})

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise UnknownParameter("Can't find app_config parameter: {}".format(item))

    def __setattr__(self, key, value):
        if key not in dir(self):
            self[key] = value
        else:
            self.__dict__[key] = value

    def __getitem__(self, item):
        if item in self:
            return super(Config, self).__getitem__(item)
        raise UnknownParameter("Can't find app_config parameter: {}".format(item))

    def __getstate__(self):
        return tuple(self.items())

    def __setstate__(self, state):
        self.update(dict(state))

    def __repr__(self):
        return "<Config: {}>".format(id(self))

    def __str__(self):

        text = "Config: {}\n\tparams:\n{}"
        params = "\n".join("\t\t{}: {}".format(p_name, p_val) for p_name, p_val in self.items())

        return text.format(id(self), params)

    @classmethod
    def operated_update(cls, update_from, update_to, deep_update=True):
        """
        Deep update

        :param update_to: updated object
        :type update_to: dict

        :param update_from: updating object
        :type update_from: dict

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: update result
        :rtype: dict

        """

        for param, param_val in update_from.items():
            if param in update_to:

                if deep_update and isinstance(param_val, dict):
                    update_to[param] = cls.operated_update(
                        update_to=update_to[param],
                        update_from=update_from[param],
                        deep_update=deep_update
                    )

            else:
                update_to[param] = param_val

        return update_to

    def reload_config(self, new_config):
        """
        Reload app_config use data from new app_config

        :return: new app_config
        :rtype: Config

        """

        self.clear()
        self.update(new_config)

        return self

    def load_from_file(self, file_path, loader, validator=EmptyValidator, deep_update=False):
        """
        Load from file (module / yaml / json / .env e.t.c)

        :param file_path: the path with filename
        :type file_path: str

         :param loader: file loader
        :type loader: any

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        # un-find path
        if not ntpath.isfile(file_path):
            raise FileNotFoundException(
                f"The {loader.alias} file is not exists on path: {file_path}"
            )

        return self.operated_update(
            update_to=self,
            update_from=validator.check(loader.load(file_path=file_path)),
            deep_update=deep_update
        )

    def from_env(self, validator=EmptyValidator, deep_update=False):
        """
        Update app_config data from environment

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        return self.operated_update(
            update_to=self,
            update_from=validator.check(ENVLoader.load()),
            deep_update=deep_update
        )

    def from_obj(self, obj, validator=EmptyValidator, deep_update=False):
        """
        Update app_config data from python object

        :param obj: python object
        :type obj: any

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        return self.operated_update(
            update_to=self,
            update_from=validator.check(ObjectLoader.load(obj=obj)),
            deep_update=deep_update
        )

    def from_module(self, file_path, validator=EmptyValidator, deep_update=False):
        """
        Update app_config data from python module

        :param file_path: the path with filename
        :type file_path: str

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        return self.load_from_file(
            file_path=file_path,
            loader=ModuleLoader,
            validator=validator,
            deep_update=deep_update
        )

    def from_yaml(self, file_path, validator=EmptyValidator, deep_update=False):
        """Update app_config data from yaml file

        :param file_path: the path with filename
        :type file_path: str

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        return self.load_from_file(
            file_path=file_path,
            loader=YamlLoader,
            validator=validator,
            deep_update=deep_update
        )

    def from_dotenv(self, file_path, validator=EmptyValidator, deep_update=False):
        """Update app_config data from yaml file

        :param file_path: the path with filename
        :type file_path: str

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        return self.load_from_file(
            file_path=file_path,
            loader=DotENVLoader,
            validator=validator,
            deep_update=deep_update
        )

    def from_json(self, file_path, validator=EmptyValidator, deep_update=False):
        """Update app_config data from json file

        :param file_path: the path with filename
        :type file_path: str

        :param validator: validator to validate app_config data
        :type validator: AbstractValidator

        :param deep_update: flag to use deep update logic
        :type deep_update: bool

        :return: updated app_config
        :rtype: Config

        """

        return self.load_from_file(
            file_path=file_path,
            loader=JSONLoader,
            validator=validator,
            deep_update=deep_update
        )

    def sub_config(self, sub_path):
        """
        Create sub_config from current app_config

        :param sub_path: jmespath standard path
        :type sub_path: str

        :return: sub app_config
        :rtype: Config

        """

        try:

            new_config_data = jmespath.search(sub_path, self)

        except jmespath.exceptions.EmptyExpressionError:

            raise ConfigException(f"Can't find sub-path: '{sub_path}'")

        return self.reload_config(new_config=new_config_data)

    def remove_prefix(self, prefix):
        """
        Remove prefix from app_config parameters

        :param prefix: app_config parameters prefix
        :type prefix: str

        :return: new app_config
        :rtype: Config

        """

        new_config_data = {}
        for param_name, param_value in self.items():
            if param_name.startswith(prefix):
                new_config_data[param_name.replace("{}_".format(prefix), "")] = param_value
            else:
                new_config_data[param_name] = param_value

        return self.reload_config(new_config=new_config_data)

    def remove_with_prefix(self, prefix, inversion=False):
        """
        Remove parameters starts with app_config prefix or any others parameters

        :param prefix: app_config parameters prefix
        :type prefix: str

        :param inversion: remove inversion flag:
            True: remove all parameters without prefix
            False: remove all parameters with prefix
        :type inversion: bool

        :return: new app_config
        :rtype: Config

        """

        new_config_data = {}
        for param_name, param_value in self.items():

            # add only with prefix
            if param_name.startswith(prefix) and inversion:
                new_config_data[param_name] = param_value

            # add only without prefix
            elif not param_name.startswith(prefix) and not inversion:
                new_config_data[param_name] = param_value

        return self.reload_config(new_config=new_config_data)

    def add_with_prefix(self, prefix, inversion=False):
        """
        Add parameters starts with app_config prefix or any others parameters

        :param prefix: app_config parameters prefix
        :type prefix: str

        :param inversion: add inversion flag
            True: add all parameters without prefix
            False: add all parameters with prefix
        :type inversion: bool

        :return: new app_config
        :rtype: Config

        """

        new_config_data = {}
        for param_name, param_value in self.items():

            # add only with prefix
            if param_name.startswith(prefix) and not inversion:
                new_config_data[param_name] = param_value

            # add only without prefix
            elif not param_name.startswith(prefix) and inversion:
                new_config_data[param_name] = param_value

        return self.reload_config(new_config=new_config_data)
