import json
import logging
import multiprocessing


def get_level_by_name(level, default=logging.INFO):
    """
    Get logging level code by level name or default level if cant find

    :param level: logging level
    :type level: str | int

    :param default: default log level
    :type default: int

    :return: logging level
    :rtype: int

    """

    return (
        getattr(logging, "_nameToLevel").get(level.upper(), default)
        if isinstance(level, str)
        else level
    )


def filter_by_send_use_handlers(record, handler_name):
    """
    Special filter to filter app_logger record use special record field '_skip_handlers'

    :param record: app_logger formatted record
    :type record: LogRecord

    :param handler_name: check handler name
    :type handler_name: str

    :return: flag to send message via handler
    :rtype: bool

    """

    # search handler from param
    skip_handlers = getattr(record, "_skip_handlers", None)

    # search handler direct in message body and set it as record.attr
    if not skip_handlers:

        # str: try to load
        if isinstance(record.msg, str):
            try:
                raw_msg = json.loads(record.msg)
            except json.JSONDecodeError:
                raw_msg = {"event": record.msg}

        # list: do not any
        elif isinstance(record.msg, list):
            raw_msg = record.msg

        # dict: add event sub-dict
        elif isinstance(record.msg, dict):
            raw_msg = {
                "event": record.msg,
                "_skip_handlers": record.msg.pop("_skip_handlers", None)
            }
        else:
            raw_msg = {"event": record.msg}

        # get skip_handlers key from msg
        extend_handlers = raw_msg.pop("_skip_handlers", None)

        # set for next handlers as record.attr
        if extend_handlers:
            setattr(record, "_skip_handlers", extend_handlers)

    # one str handler convert to list
    if isinstance(skip_handlers, str):
        skip_handlers = [skip_handlers]

    return handler_name not in (skip_handlers or [])


def create_proc_msg(log_msg):
    """
    Create msg with multiprocessing process name

    :param log_msg: log message
    :type: dict or str

    :return: updated log msg
    :rtype: dict or str

    """

    # for multiprocessing logs
    proc = multiprocessing.current_process()
    if proc.name != "MainProcess":

        # msg as dict: add param
        if isinstance(log_msg, dict):
            log_msg["proc_name"] = proc.name

        # msg as str: add prefix
        elif isinstance(log_msg, str):
            log_msg = f"{proc.name}: {log_msg}"

    return log_msg
