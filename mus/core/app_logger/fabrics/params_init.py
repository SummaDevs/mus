import logging
import sys
from functools import partial

from ..formatters.json_formatter import JsonFormatter
from ..handlers.http_handler import HumanHTTPHandler
from ..helpers import get_level_by_name, filter_by_send_use_handlers


def init_logging(
        name=None,
        log_std=...,
        log_file=...,
        log_http=...,
        as_json=False,
        propagate=None,
):
    """
    logging init (if already exists by name: return exists without reconfiguration)

    :param name: app_logger namespace
    :type name: str

    :param log_std: app_config to log to stdout
        {
            "level": not required [default: logging.INFO]
        }
    :type log_std: dict

    :param log_file: app_config to save log to file
        {
            "filename": required,
            "level": not required [default: logging.INFO]
        }
    :type log_file: dict

    :param log_http: http info to send log
        {
            "url": required,
            "token": required,
            "level": not required [default: logging.INFO]
        }
    :type log_http: dict

    :param as_json: format response as json flag
    :type as_json: bool

    :param propagate: Sent log messages to root app_logger if True, keep silence otherwise
    :type propagate: Optional[bool]

    :return: configured app_logger
    :rtype: logging.Logger

    """

    # create app_logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if propagate is not None:
        logger.propagate = propagate

    # already configured
    if logger.handlers:
        return logger

    # format set
    if as_json:
        formatter = JsonFormatter(
            '{'
            '"datetime":"%(asctime)s",'
            '"levelname":"%(levelname)s",'
            '"filename":"%(filename)s",'
            '"lineno":"%(lineno)d",'
            '"message":%(message)s'
            '}',
            "%Y-%m-%dT%H:%M:%S+00:00"
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s '
            '%(levelname)s '
            '%(filename)s '
            '%(lineno)d '
            '%(message)s',
            "%Y-%m-%dT%H:%M:%S+00:00"
        )

    # handlers
    exists_handlers = {}

    # stream handler: always active
    if log_std is ...:
        log_std = {
            "level": "INFO"
        }

    # stream handler
    if log_std is not ...:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(
            get_level_by_name(
                level=log_std.get("level"),
                default=logging.INFO
            )
        )
        stream_handler.setFormatter(formatter)
        if as_json:
            stream_handler.addFilter(
                partial(
                    filter_by_send_use_handlers,
                    handler_name="stream"
                )
            )
        exists_handlers["stream"] = stream_handler

    # file handler
    if log_file is not ...:
        file_handler = logging.FileHandler(filename=log_file["filename"])
        file_handler.setLevel(
            get_level_by_name(
                level=log_file.get("level"),
                default=logging.INFO
            )
        )
        file_handler.setFormatter(formatter)
        if as_json:
            file_handler.addFilter(
                partial(
                    filter_by_send_use_handlers,
                    handler_name="file"
                )
            )
        exists_handlers["file"] = file_handler

    # http handler
    if log_http is not ...:

        if not as_json:
            raise ValueError("HTTP Handler can use only with as_json")

        http_handler = HumanHTTPHandler(
            url=log_http["url"],
            token=log_http["token"]
        )
        http_handler.setLevel(
            get_level_by_name(
                level=log_http.get("level"),
                default=logging.INFO
            )
        )
        http_handler.setFormatter(formatter)
        http_handler.addFilter(
            partial(
                filter_by_send_use_handlers,
                handler_name="http"
            )
        )
        exists_handlers["http"] = http_handler

    # set all exists handlers
    for handler_name in exists_handlers:
        logger.addHandler(exists_handlers[handler_name])

    return logging.getLogger(name)
