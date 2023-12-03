import logging
import os

from mus.config.config import app_config

SKIP_FILE_SET = {
    "_stats.json",  # directory statistics
}

ES_DOC_EXT = ".json"

ERROR_MAX_CNT = 200
STATS_PRINT_CNT = 100

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def arc_walk_iter(text_path, stats):
    for root_dir, sub_dir, files in os.walk(text_path):

        if not files:
            continue

        for file_name in files:
            stats["cnt"] += 1

            _, short_name = os.path.split(file_name)
            if short_name in SKIP_FILE_SET:
                stats["skip_file_cnt"] += 1
                continue
            if not short_name.endswith(ES_DOC_EXT):
                stats["skip_file_ext_cnt"] += 1
                continue

            yield root_dir, file_name

            if not stats["cnt"] % STATS_PRINT_CNT:
                logger.info(stats)
                logger.info("Last file %s", os.path.join(root_dir, file_name))

            if stats["error_cnt"] == ERROR_MAX_CNT:
                logger.info(stats)
                logger.error({
                    "error": "Too many errors, please update algos",
                    "root_dir": root_dir
                })
                break
