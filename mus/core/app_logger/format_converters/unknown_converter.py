from .abstract_converter import AbstractConverter


class UnknownConverter(AbstractConverter):
    """
    Converter for unknown data type

    """

    file_types = [None]

    @classmethod
    def encode(cls, data, **kwargs):
        """
        Encode (convert from python to ...) some data

        :param data: data to encode (python format)
        :type data: any

        :return: same data
        :rtype: any

        """

        return data

    @classmethod
    def decode(cls, data, **kwargs):
        """
        Decode (convert from ... to python format) some data

        :param data: data to decode (... format)
        :type data: any

        :return: same data
        :rtype: any

        """

        return data
