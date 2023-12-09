import json
from abc import ABCMeta, abstractmethod
from datetime import datetime, date
from decimal import Decimal
from types import GeneratorType

from arrow import Arrow


class AbstractConverter(metaclass=ABCMeta):
    """
    Main abstract class for all data type converters

    """

    @property
    @abstractmethod
    def file_types(self):
        """
        Converter file types

        :return: supported file types
        :rtype: list

        """

    @classmethod
    @abstractmethod
    def encode(cls, data, **kwargs):
        """
        Encode (convert from python to converter format) some data

        :param data: data to encode (python format)
        :type data: any

        :return: encoded data (converter format)
        :rtype: any

        """

    @classmethod
    @abstractmethod
    def decode(cls, data, **kwargs):
        """
        Decode (convert from converter to python format) some data

        :param data: data to decode (converter format)
        :type data: any

        :return: decoded data (python format)
        :rtype: any

        """


class ExtendJsonEncoder(json.JSONEncoder):
    """
    Extend JSONEncoder
        :method default: extend method to encode data

    Add:
        - decimal
        - arrow
        - datetime, date
        - list, GeneratorType, set, tuple
        - object with to_python method

    """

    def default(self, data):
        """
        Main method to convert data

        :param data: convert data
        :type data: any

        :return: encoded data
        :rtype: any

        """

        # decimal
        if isinstance(data, Decimal):

            return str(data)

        # arrow
        elif isinstance(data, Arrow):

            return data.isoformat()

        # datetime
        elif isinstance(data, (datetime, date)):

            return data.isoformat()

        # sequence
        elif isinstance(data, (tuple, list, set, GeneratorType)):

            return map(self.default, data)

        # other formats
        else:
            try:

                return json.JSONEncoder.default(self, data)

            except TypeError:

                return f"{data}"
