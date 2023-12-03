import logging
import os

from mus.config.config import app_config

STATS_PRINT_CNT = 10
ERROR_MAX_CNT = 1000

logger = logging.getLogger(app_config["PROJECT_NAME"])

skip_dir_path = {
    ".git",
}


def unarc_walk_iter(arc_path, text_path, dir_func, stats):
    for root_dir, sub_dir, files in os.walk(arc_path):

        if not dir_func(stats, arc_path, root_dir, text_path, sub_dir, files):
            logger.info("Skip process directory %s", root_dir)
            continue

        if any((skip in sub_dir for skip in skip_dir_path)):
            sub_dir[:] = [sdr for sdr in sub_dir if sdr not in skip_dir_path]
            logger.info("Skip sub dir %s", str(skip_dir_path))

        if not files:
            continue

        for file_name in files:
            stats["cnt"] += 1

            yield text_path, root_dir, file_name

            if not stats["cnt"] % STATS_PRINT_CNT:
                logger.info(stats)

            if stats["error_cnt"] > ERROR_MAX_CNT:
                logger.info(stats)
                logger.error({
                    "error": "Too many errors, please update algos",
                    "root_dir": root_dir
                })
                break
