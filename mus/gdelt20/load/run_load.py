from mus.config.config import app_config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


def check_params(start_date, finish_date):
    assert start_date <= finish_date, f"{start_date} gt {finish_date}"


def run_load(_, base_path, target_service, start_date, finish_date, languages, obj_types):
    check_params(start_date, finish_date)
    _ = base_path, target_service, start_date, finish_date, languages, obj_types

    if target_service == "s3":
        logger.info("Load target AWS S3 bucket")
    elif target_service == "cs":
        logger.info("Load target GCP Cloud Storage bucket")
    elif target_service == "es":
        logger.info("Load target ElasticSearch")
    elif target_service == "db":
        logger.info("Load target data base")
    elif target_service == "avro":
        logger.info("Load target avro files")
    else:
        raise NotImplementedError(f"Target {target_service} is not implemented")
