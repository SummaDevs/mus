import logging
import os

from mus.cleansing.unstruct.unstruct_part import extract_text
from mus.config.config import app_config
from mus.constant import cons_cleansing
from mus.core.file_utils.file_utils import get_file_desc
from mus.core.file_utils.file_utils import save_file_text
from mus.core.file_utils.path_utils import get_target_full_name

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def analyse_arc_file(arc_path, text_path, root_dir, file_name, stats):
    file_path = os.path.join(root_dir, file_name)
    # TODO: should be parametrized, some info can be skipped
    if os.path.isfile(get_target_full_name(text_path, file_path)):
        stats["target_exists"] += 1
        return

    file_ext = file_name.rsplit(".", 1)[-1].lower()
    if file_ext not in cons_cleansing.TYPE_EXTRACT_EXT_SET:
        stats["skipped_by_extension"] += 1
        return

    logger.info("Analyse file %s", file_path)

    file_desc = get_file_desc(arc_path, file_path, file_ext)
    # TODO: use heuristics to handle big files
    if file_desc["extract_text"]:
        if file_desc["file_size_kb"] > cons_cleansing.UNS_FILE_SIZE_MAX_KB:
            logger.info("File %s size > %s KB, skip", file_path, cons_cleansing.UNS_FILE_SIZE_MAX_KB)
            stats["skip_big_file_cnt"] += 1
            return

        text_meta, file_text = extract_text(file_path, file_ext)
        stats["extract_text_cnt"] += 1
    else:
        stats["no_text_type_cnt"] += 1
        return

    if "error_msg" in text_meta:
        stats["error_cnt"] += 1
        text_meta["file_rel_path"] = file_path.removeprefix(arc_path)
        logger.error(text_meta)
        return

    save_file_text(
        stats,
        arc_path,
        text_path,
        file_path,
        file_desc,
        text_meta,
        file_text
    )
