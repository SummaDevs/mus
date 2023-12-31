import logging

from mus.config.config import app_config
from mus.gdelt20.extract.extractor import Gdelt20Extractor
from mus.gdelt20.extract.file_list_gen import Gdelt20FileListGen
from mus.gdelt20.extract.gd_dir_tree import create_path_tree

logger = logging.getLogger(app_config["PROJECT_NAME"])


def check_params(start_date, finish_date):
    assert start_date <= finish_date, f"{start_date} gt {finish_date}"


def run_extract_gdelt(config_obj, base_path, start_date, finish_date, languages, obj_types):
    check_params(start_date, finish_date)

    create_path_tree(base_path, start_date, finish_date, languages, obj_types)
    logger.info("Creating path tree")

    logger.info("Creating file lists")
    Gdelt20FileListGen(
        config_obj,
        base_path,
        start_date,
        finish_date,
        languages,
        obj_types
    )()

    logger.info("Extracting files")
    Gdelt20Extractor(
        config_obj,
        base_path,
        start_date,
        finish_date,
        languages,
        obj_types
    )()

    logger.info("Gdelt20 data extraction finished")
