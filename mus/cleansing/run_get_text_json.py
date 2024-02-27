import os
import logging
from collections import defaultdict
from pathlib import Path
from magika import Magika

from mus.cleansing.unstruct.analyse_arc_file import analyse_arc_file
from mus.cleansing.unstruct.unstruct_part import is_unstructured_installed
from mus.config.config import app_config
from mus.core.arc_walk.arc_walk import arc_walk_iter
from mus.core.file_utils.file_utils import save_dir_meta

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def run_get_text_json(_, arc_path, text_path, is_debug=False):
    is_installed, el_list = is_unstructured_installed()
    if not is_installed:
        logger.error(el_list)
        logger.error(
            "Please install unstructured dependencies. "
            "See for details "
            "https://unstructured-io.github.io/unstructured/installation"
            "/full_installation.html")
        return

    stats = defaultdict(int)
    mag = Magika()

    logger.info("Start walking in %s out %s", arc_path, text_path)

    for text_path, root_dir, file_name in arc_walk_iter(arc_path, text_path, save_dir_meta, stats):
        if is_debug:
            file_path = os.path.join(root_dir, file_name)
            file_desc = mag.identify_path(Path(str(file_path)))
            logger.debug(
                "%s: %s, score - %s, type - %s, label - %s, group - $s",
                file_desc.path,
                file_desc.dl.magic,
                file_desc.dl.score,
                file_desc.dl.mime_type,
                file_desc.dl.ct_label,
                file_desc.dl.group
            )

        analyse_arc_file(arc_path, text_path, root_dir, file_name, stats)

    logger.info(stats)
    logger.info("Exit walk")
