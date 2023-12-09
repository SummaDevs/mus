import json

import ndjson

from .abstract_converter import AbstractConverter, ExtendJsonEncoder


class ExtendNDJSONEncoder(ExtendJsonEncoder):
    """
    Extend NDJSONEncoder
        :method encode: extend method to encode data

    Add:
        - decimal
        - arrow
        - datetime, date
        - list, GeneratorType, set, tuple
        - object with to_python method

    """

    def encode(self, obj):
        """
        Convert python object to nd-json format

        :param obj: python object
        :type obj: sequence

        :return: nd-json object
        :rtype: str

        """

        return '\n'.join(map(super().encode, obj))


class NDJSONConverter(AbstractConverter):
    """
    Converter for nd-json data type

    """

    file_types = [
        "jl",
        "ndjson"
    ]

    @classmethod
    def encode(cls, data, **kwargs):
        """
        Encode (convert from python to nd-json format) some data

        :param data: data to encode (python format)
        :type data: any

        :return: encoded data (nd-json format)
        :rtype: bytearray

        """

        return json.dumps(data, cls=ExtendNDJSONEncoder).encode("utf-8")

    @classmethod
    def decode(cls, data, **kwargs):
        """
        Decode (convert from nd-json to python format) some data

        :param data: data to decode (nd-json format)
        :type data: any

        :return: decoded data (python format)
        :rtype: any

        """

        return ndjson.loads(data)
