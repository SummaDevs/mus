import json

from .abstract_converter import AbstractConverter, ExtendJsonEncoder


class JSONConverter(AbstractConverter):
    """
    Converter for json data type

    """

    file_types = [
        "json"
    ]

    @classmethod
    def encode(cls, data, **kwargs):
        """
        Encode (convert from python to json format) some data

        :param data: data to encode (python format)
        :type data: any

        :return: encoded data (json format)
        :rtype: bytearray

        """

        return json.dumps(data, cls=ExtendJsonEncoder).encode("utf-8")

    @classmethod
    def decode(cls, data, **kwargs):
        """
        Decode (convert from json to python format) some data

        :param data: data to decode (json format)
        :type data: any

        :return: decoded data (python format)
        :rtype: any

        """

        return json.loads(data)
