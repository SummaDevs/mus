import trafaret as t
from trafaret.keys import subdict

from mus.core.text.str_utils import str_strip


def db_credentials_schema(prefix=""):
    """
    Template to striped string

    :param prefix: special prefix to get db config
    :type prefix: str

    :return: db config schema
    :rtype: t.Dict

    """

    return t.Dict({
        t.Key(f"{prefix}DB_USER", optional=True) >> "DB_USER":
            str_strip(min_length=1, max_length=64),
        t.Key(f"{prefix}DB_PASS", optional=True) >> "DB_PASS":
            str_strip(min_length=1, max_length=64),
        t.Key(f"{prefix}DB_HOST", optional=True) >> "DB_HOST":
            str_strip(min_length=1, max_length=256),
        t.Key(f"{prefix}DB_PORT", optional=True) >> "DB_PORT":
            t.Int(gte=1024, lte=65000),
        t.Key(f"{prefix}DB_NAME", optional=True) >> "DB_NAME":
            str_strip(min_length=2, max_length=64),
        t.Key(f"{prefix}DB_POOL_SIZE", optional=True, ) >> "DB_POOL_SIZE":
            t.Int(gte=1, lte=128),
        t.Key(f"{prefix}DB_MAX_OVERFLOW", optional=True) >> "DB_MAX_OVERFLOW":
            t.Int(gte=1, lte=128),
        t.Key(f"{prefix}DB_ECHO", optional=True) >> "DB_ECHO":
            (t.Null() | t.Bool()) >> bool
    })


def logger_schema(prefix=""):
    """
    Template to work with logger config full example:

        LOGGER:
            STREAM_LEVEL: INFO
            FILE_NAME: app_log.log
            FILE_LEVEL: INFO
            HTTP_URL: https://logging.com
            HTTP_TOKEN: my_token
            HTTP_LEVEL: INFO

    :param prefix: special prefix to get logger config
    :type prefix: str

    :return: logger config validator
    :rtype: t.Dict

    """

    levels = t.Enum(
        "CRITICAL",
        "FATAL",
        "ERROR",
        "WARN",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET"
    )

    return t.Dict(
        t.Key(
            name=f"{prefix}LOGGING_LEVEL",
            to_name="LOGGING_LEVEL",
            optional=True,
            trafaret=levels
        ),

        # stream logger
        subdict(
            "STREAM",
            t.Key(
                name=f"{prefix}STREAM_LEVEL",
                to_name="STREAM_LEVEL",
                optional=True,
                trafaret=levels
            ),
            trafaret=lambda x: x
        ),
    )


def es_credentials_schema(prefix=""):
    """
    :param prefix: special prefix to get es config
    :type prefix: str

    :return: elasticsearch config schema
    :rtype: t.Dict

    """

    return t.Dict({
        t.Key(f"{prefix}ES_USER", optional=True) >> "ES_USER":
            str_strip(min_length=1, max_length=64),
        t.Key(f"{prefix}ES_PASS", optional=True) >> "ES_PASS":
            str_strip(min_length=1, max_length=64),
        t.Key(f"{prefix}ES_HOST", optional=True) >> "ES_HOST":
            str_strip(min_length=1, max_length=256),
        t.Key(f"{prefix}ES_HOST_SCHEMA", optional=True) >> "ES_HOST_SCHEMA":
            str_strip(min_length=1, max_length=8),
        t.Key(f"{prefix}ES_PORT", optional=True) >> "ES_PORT":
            t.Int(gte=1024, lte=65000),
        t.Key(f"{prefix}ES_NODES_NUM", optional=True) >> "ES_NODES_NUM":
            t.Int(gte=1, lte=128)
    })


def openai_schema(prefix=""):
    """
    :param prefix: special prefix to get es config
    :type prefix: str

    :return: openai config schema
    :rtype: t.Dict

    """

    return t.Dict({
        t.Key(f"{prefix}OPENAI_API_KEY", optional=True) >> "OPENAI_API_KEY":
            str_strip(min_length=64, max_length=64),
    })
