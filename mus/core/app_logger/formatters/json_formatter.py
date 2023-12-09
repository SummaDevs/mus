import json
import logging

from ..format_converters.abstract_converter import ExtendJsonEncoder


class JsonFormatter(logging.Formatter):
    """
    Patch formatter to return message body always as json dumps string

    """

    def format(self, record):
        """
        Redefine format method to always send json as message body

        :param record: app_logger record object
        :type record: LogRecord

        :return: formatted message
        :rtype: str

        """

        # check type in first call
        if getattr(record, "asctime", None) is None:
            if isinstance(record.msg, (dict, list, tuple)):
                record.msg = json.dumps(record.msg, cls=ExtendJsonEncoder)
            else:
                record.msg = {"event": str(record.msg)}

        return super().format(record)
