import logging

from mus.config.config import app_config

logger = logging.getLogger(app_config["PROJECT_NAME"])


def run_load_gdelt(_, base_path, target_service, start_date, finish_date, languages, obj_types):
    _ = base_path, target_service, start_date, finish_date, languages, obj_types

    match target_service:
        case "s3":
            logger.info("Load target AWS S3 bucket")
        case "cs":
            logger.info("Load target GCP Cloud Storage bucket")
        case "es":
            logger.info("Load target ElasticSearch")
        case "db":
            logger.info("Load target data base")
        case "avro":
            logger.info("Load target avro files")
        case _:
            raise NotImplementedError(f"Target {target_service} is not implemented")
