import logging
import os

from mus.config.config import app_config
from mus.constant.cons_cleansing import ERROR_MAX_CNT
from mus.constant.cons_cleansing import STATS_PRINT_CNT
from mus.constant.cons_cleansing import skip_dir_path

logger = logging.getLogger(app_config["PROJECT_NAME"])


def check_progress(cnt_key, root_dir, file_name, stats, error_max_count=ERROR_MAX_CNT, file_max_cnt=None):
    stats[cnt_key] += 1

    if not stats[cnt_key] % STATS_PRINT_CNT:
        logger.info(stats)
        logger.info("Last file %s", os.path.join(root_dir, file_name))

    if stats["error_cnt"] >= error_max_count:
        logger.info(stats)
        logger.error({
            "error": "Too many errors, please update algos",
            "root_dir": root_dir
        })
        return False

    if file_max_cnt is not None and stats[cnt_key] >= file_max_cnt:
        logger.info(stats)
        logger.warning("Number of files has reached limit %s", file_max_cnt)
        return False

    return True


def arc_walk_iter(arc_path, text_path, dir_func, stats):
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
            if not check_progress("cnt", root_dir, file_name, stats):
                return

            yield text_path, root_dir, file_name
