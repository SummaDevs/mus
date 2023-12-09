import logging

from .params_init import init_logging


def init_logger_from_config(name, config):
    """
    Init app_logger from app_config (if already exists by name: return exists without reconfiguration)

    :param name: app_logger name
    :type name: str

    :param config: app_config object
    :type config: any

    :return: configured app_logger
    :rtype: logging.Logger

    """

    logger = logging.getLogger(name)

    # already configured
    if logger.handlers:
        return logger

    # get logging app_config
    init_params = {}
    logging_config = config.get("LOGGER")

    if not logging_config:
        return init_logging(
            name=name,
            as_json=True
        )

    try:

        # stream handler
        if logging_config.get("STREAM"):
            init_params["log_std"] = {
                "level": logging_config["STREAM"]["STREAM_LEVEL"]
            }

        # file handler
        if logging_config.get("FILE"):
            init_params["log_file"] = {
                "filename": logging_config["FILE"]["FILE_NAME"],
                "level": logging_config["FILE"].get("FILE_LEVEL", "INFO")
            }

        # http handler
        if logging_config.get("HTTP"):
            init_params["log_http"] = {
                "url": logging_config["HTTP"]["HTTP_URL"],
                "token": logging_config["HTTP"]["HTTP_TOKEN"],
                "level": logging_config["HTTP"].get("HTTP_LEVEL", "INFO")
            }

        # es handler
        if logging_config.get("ES"):
            init_params["log_es"] = {
                "host": logging_config["ES"]["ES_HOST"],
                "port": logging_config["ES"]["ES_PORT"],
                "index": logging_config["ES"]["ES_INDEX"],
                "region": logging_config["ES"].get("ES_REGION"),
                "use_ssl": logging_config["ES"].get("ES_USE_SSL"),
                "raise_exc": logging_config["ES"].get("ES_RAISE_EXC"),
                "extra": logging_config["ES"].get("ES_EXTRA"),
                "level": logging_config["ES"].get("ES_LEVEL", "INFO"),
                "flush_frequency": logging_config["ES"].get("ES_FLUSH_FRQ"),
                "buffer_size": logging_config["ES"].get("ES_BUFFER_SIZE")
            }

    except KeyError as e:
        raise ValueError(
            f"Can't find expect key {e} for app_logger handler init") from e

    return init_logging(
        name=name,
        **init_params,
        as_json=True,
        propagate=logging_config.get("PROPAGATE"),
    )
