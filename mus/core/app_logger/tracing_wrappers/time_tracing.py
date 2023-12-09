import inspect
import logging
import ntpath
from datetime import timedelta
from functools import partial

import arrow

from ..helpers import get_level_by_name, create_proc_msg


class TimeTracingLogger:
    """
    Tracing time app_logger

    """

    logger_level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "warn": logging.WARNING,
        "error": logging.ERROR,
        "exception": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.start = arrow.utcnow()

        self._is_first = True
        self._create_msg_fabric = create_proc_msg

        # patch to add frame extra
        self.logger.makeRecord = self.make_record

    def __getattr__(self, item):
        level = TimeTracingLogger.__dict__["logger_level"].get(item)
        if level:
            return partial(self, level=level)

        return self.__dict__[item]

    def make_record(self, *args, **kwargs):
        """
        Patch makeRecord in app_logger to can insert some extra data to log rv body

        """

        # search frame extra in extra data
        frame_extra = {}
        for arg in args:
            if isinstance(arg, dict) and set(arg.keys()) & {"lineno", "filename"}:
                frame_extra["lineno"] = arg.pop("lineno")
                frame_extra["filename"] = arg.pop("filename")

        # create record use standard app_logger
        rv = logging.Logger.makeRecord(self.logger, *args, **kwargs)

        # update record by frame extra
        if frame_extra is not None:
            rv.__dict__.update(frame_extra)

        return rv

    def __call__(self, log_msg, level=None):
        """
        Send time tracing log message

        :param log_msg: log message
        :type log_msg: dict or str

        :param level: app_logger message level
        :type level: str

        """

        # first message: no timedelta
        if self._is_first:
            self._is_first = False

        # log msg as dict: add param
        time_delta = str(timedelta(seconds=(arrow.utcnow() - self.start).seconds))
        if isinstance(log_msg, dict):
            log_msg["timedelta"] = time_delta

        # log msg as dict: add postfix
        elif isinstance(log_msg, str):
            log_msg = f"{log_msg}: {time_delta}"

        # send log message
        self.logger.log(
            level=get_level_by_name(
                level=level,
                default=logging.INFO
            ),
            msg=self._create_msg_fabric(log_msg=log_msg),

            # add real frame data
            extra={
                "lineno": inspect.currentframe().f_back.f_lineno,
                "filename": ntpath.basename(inspect.currentframe().f_back.f_code.co_filename)
            }
        )

    def log(self, level, msg):
        """
        Wrap main log method

        :param level: log level
        :type level: int | str

        :param msg: log message
        :type msg: any

        """

        self(
            log_msg=msg,
            level=level
        )

    def register_create_msg_fabric(self, fabric):
        """
        Register fabric use to create log msg

        :param fabric: fabric to create log msg
        :type fabric: callable

        """

        if not callable(fabric):
            raise ValueError(f"Fabric is must be callable, but get {fabric}")

        self._create_msg_fabric = fabric

    @classmethod
    def create(cls, name):
        """
        Create time tracing app_logger instance

        :param name: app_logger name
        :type name: app_logger name

        :return: configured time tracing app_logger instance
        :rtype: TimeTracingLogger

        """

        return cls(name=name)


# alias on TimeTracingLogger init
get_time_tracing_logger = TimeTracingLogger.create
