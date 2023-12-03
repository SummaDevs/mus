from abc import ABCMeta, abstractmethod


class AbstractClassProperty:
    """
    Special class to create abstract property

    """

    def __init__(self, expect=None):
        self.expect = expect

        self.name = None
        self.owner = None

    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

    def __set__(self, instance, value):
        raise NotImplementedError(
            f"Redefine attribute '{self.name}' in class '{self.owner.__name__}'"
            f" expect {self.expect}" if self.expect else ""
        )

    def __get__(self, instance, owner):
        raise NotImplementedError(
            f"Redefine attribute '{self.name}' in class '{self.owner.__name__}'"
            f" expect {self.expect}" if self.expect else ""
        )


class AbstractLoader(metaclass=ABCMeta):
    """
    Abstract class for all app_config loaders

    """

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        """
        Load app_config data from resource

        :return: app_config data
        :rtype: dict

        """


class AbstractValidator(metaclass=ABCMeta):
    """
    Abstract class for app_config validators

    """

    @classmethod
    @abstractmethod
    def check(cls, config_data):
        """
        Validate app_config data

        :param config_data: app_config data to validate
        :type config_data: dict

        :return: validate data
        :rtype: dict

        """


class EmptyValidator(AbstractValidator):
    """
    Validator to do not validate anything

    """

    @classmethod
    def check(cls, config_data):
        """
        Do not validate app_config data

        :param config_data: app_config data to validate
        :type config_data: dict

        :return: validate data
        :rtype: dict

        """

        return config_data
