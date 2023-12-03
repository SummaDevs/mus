import trafaret as t
from trafaret.keys import subdict


def str_strip(nullable=False, allow_blank=False, min_length=None, max_length=None):
    """
    Striped string

    :param nullable: flag that string can be nullable
    :type nullable: bool

    :param allow_blank: special flag that string can be blank
    :type allow_blank: bool

    :param min_length: min string length
    :type min_length: int

    :param max_length: max string length
    :type max_length: int

    :return: stripped string validator
    :rtype: t.Trafaret

    """

    main = t.String(allow_blank=allow_blank, min_length=min_length, max_length=max_length)

    return t.Null() | (main >> str.strip) if nullable else main >> str.strip


def url(body_re=""):
    """
    Template to parse URL

    :param body_re: special body regexp
    :type body_re: str

    :return: url validator
    :rtype: t.Regexp

    """

    return t.Regexp(f"^(http|https)://({body_re}).*")


def logger_config(prefix=""):
    """
    Template to work with app_logger app_config
        full example:

        STREAM_LEVEL: INFO
        FILE_NAME: app_log.log
        FILE_LEVEL: INFO
        HTTP_URL: https://logging.com
        HTTP_TOKEN: my_token
        HTTP_LEVEL: INFO
        ES_HOST: https://es.com
        ES_PORT: 5420
        ES_INDEX: log_index
        ES_REGION: us-east-1
        ES_USE_SSL: false
        ES_RAISE_EXC: false
        ES_LEVEL: INFO
        ES_EXTRA:
            DATA: some extra data

    :param prefix: special prefix to get app_logger app_config
    :type prefix: str

    :return: app_logger app_config validator
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

        # 'propagate' app_logger flag

        t.Key(
            name=f"{prefix}PROPAGATE",
            to_name="PROPAGATE",
            optional=True,
            trafaret=t.ToBool(),
        ),

        # stream app_logger
        subdict(
            "STREAM",
            t.Key(
                name=f"{prefix}STREAM_LEVEL",
                to_name="STREAM_LEVEL",
                trafaret=levels,
                default="INFO"
            ),
            trafaret=lambda x: x
        ),

        # file app_logger
        subdict(
            "FILE",
            t.Key(
                name=f"{prefix}FILE_NAME",
                to_name="FILE_NAME",
                optional=True,
                trafaret=str_strip(nullable=True, min_length=2, max_length=64),
            ),
            t.Key(
                name=f"{prefix}FILE_LEVEL",
                to_name="FILE_LEVEL",
                optional=True,
                trafaret=levels
            ),
            trafaret=lambda x: x
        ),

        # http app_logger
        subdict(
            "HTTP",
            t.Key(
                name=f"{prefix}HTTP_URL",
                to_name="HTTP_URL",
                optional=True,
                trafaret=str_strip(min_length=1),
            ),
            t.Key(
                name=f"{prefix}HTTP_TOKEN",
                to_name="HTTP_TOKEN",
                optional=True,
                trafaret=str_strip(min_length=2, max_length=128)
            ),
            t.Key(
                name=f"{prefix}HTTP_LEVEL",
                to_name="HTTP_LEVEL",
                optional=True,
                trafaret=levels
            ),
            trafaret=lambda x: x
        ),

        # es app_logger
        subdict(
            "ES",
            t.Key(
                name=f"{prefix}ES_HOST",
                to_name="ES_HOST",
                optional=True,
                trafaret=str_strip(min_length=1),
            ),
            t.Key(
                name=f"{prefix}ES_PORT",
                to_name="ES_PORT",
                optional=True,
                trafaret=t.Int(gt=0)
            ),
            t.Key(
                name=f"{prefix}ES_INDEX",
                to_name="ES_INDEX",
                optional=True,
                trafaret=str_strip(min_length=2, max_length=32)
            ),
            t.Key(
                name=f"{prefix}ES_REGION",
                to_name="ES_REGION",
                optional=True,
                trafaret=str_strip(min_length=8, max_length=12)
            ),
            t.Key(
                name=f"{prefix}ES_USE_SSL",
                to_name="ES_USE_SSL",
                optional=True,
                trafaret=t.ToBool()
            ),
            t.Key(
                name=f"{prefix}ES_RAISE_EXC",
                to_name="ES_RAISE_EXC",
                optional=True,
                trafaret=t.ToBool()
            ),
            t.Key(
                name=f"{prefix}ES_EXTRA",
                to_name="ES_EXTRA",
                optional=True,
                trafaret=t.Dict({}, allow_extra="*")
            ),
            t.Key(
                name=f"{prefix}ES_LEVEL",
                to_name="ES_LEVEL",
                optional=True,
                trafaret=levels
            ),
            t.Key(
                name=f"{prefix}ES_FLUSH_FRQ",
                to_name="ES_FLUSH_FRQ",
                optional=True,
                trafaret=t.Int(gt=0)
            ),
            t.Key(
                name=f"{prefix}ES_BUFFER_SIZE",
                to_name="ES_BUFFER_SIZE",
                optional=True,
                trafaret=t.Int(gt=0)
            ),
            trafaret=lambda x: x
        )

    )
