"""
Base config abstract class.
Define config class structure and interface.

"""
import abc
from collections import ChainMap
from copy import deepcopy

from .base_schema import TrafaretConfigSchemaBase


class BaseConfig(abc.ABC):
    """
    Base config.
    Main "load" method should be overwritten in child classes.
    Use "schema" to validate and build config with required structure.
    "schema" should be based on "TrafaretConfigSchemaBase" class.
    Init **kwargs arguments can be used to add extra fields to config before validation.
    "update" method arguments can be used to add extra fields to config after validation.

    """

    def __init__(self, schema=None, **kwargs):
        loaded_data = self.load()
        loaded_data.update(**kwargs)
        self._data = self.validate(schema, loaded_data)

    @staticmethod
    def validate(schema, loaded_data):
        """
        Validate loaded raw config data against given schema.
        Leave loaded data "as is" if no schema provided.

        :param schema: Validation schema
        :type schema: TrafaretConfigSchemaBase

        :param loaded_data: Raw loaded data
        :type loaded_data: dict[Any]

        :return: Validated config data
        :rtype: dict[Any]

        """
        if schema and isinstance(schema, TrafaretConfigSchemaBase):
            return schema.validate_and_build(loaded_data)

        return loaded_data

    @abc.abstractmethod
    def load(self):
        """
        Main method to load raws config data
        from some source.

        Should be overwritten in child classes.

        :return: Raw loaded data
        :rtype: dict[Any]

        """
        return {}

    @property
    def as_dict(self):
        """
        Convert current loaded and validated config to dict.

        :return: Config
        :rtype: dict[Any]

        """
        return deepcopy(self._data)

    def update(self, **new_data):
        """
        Update current loaded
        and validated config with extra values.

        :param new_data: Extra values
        :type new_data: dict[any]

        :return: None

        """
        self._data.update(**new_data)

    def __getattr__(self, item):
        """
        Provide access to stored data using "dot" notation.

        :param item: Attribute name
        :type item: str

        :return: Stored value by attribute
        :rtype: Any

        :raises: AttributeError if attribute was not found

        """
        settings = ChainMap(self._data, self.DEFAULTS)

        if item in settings:
            return settings[item]

        raise AttributeError(f"No such attribute: {item}")

    def __setattr__(self, key, value):
        """
        Close attribute setting to make config immutable.
        Only inner attributes can be passed.

        :param key: Attribute name
        :type key: str

        :param value: Attribute value
        :type value: Any

        :return: None

        :raises: TypeError if attribute assignment caught

        """
        if key.startswith("_"):
            super().__setattr__(key, value)

        else:
            raise TypeError(
                f"'{self.__class__.__name__}' "
                f"object does not support item assignment"
            )
