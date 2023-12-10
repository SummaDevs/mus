from mus.config.config import app_config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.gdelt20.extract.extractor import Gdelt20Extractor
from mus.gdelt20.extract.file_list_gen import Gdelt20FileListGen
from mus.gdelt20.extract.gd_dir_tree import create_path_tree

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


def check_params(start_date, finish_date):
    assert start_date <= finish_date, f"{start_date} gt {finish_date}"


def run_extract(config_obj, base_path, start_date, finish_date, languages, obj_types):
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
