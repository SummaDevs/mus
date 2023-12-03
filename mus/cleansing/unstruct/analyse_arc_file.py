import json
import logging
import os
from datetime import datetime

from mus.cleansing.unstruct import unstruct_part
from mus.cleansing.unstruct.unstruct_part import extract_text
from mus.config.config import app_config
from mus.constant import cons_cleansing
from mus.constant import constant
from mus.core.file_utils.file_utils import get_flat_filename

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def ts_to_utc(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def file_desc_dict(arc_base_dir, file_path, fstat, is_ext_text, mime_type):
    return {
        "file_path": file_path.removeprefix(arc_base_dir),
        "file_extension": os.path.splitext(file_path)[1],
        "extract_text": is_ext_text,
        "file_mime_type": mime_type,
        "file_size_kb": fstat.st_size // constant.K_BYTE,
        "datetime_access": ts_to_utc(fstat.st_atime),
        "datetime_modification": ts_to_utc(fstat.st_mtime),
        "datetime_meta": ts_to_utc(fstat.st_ctime)

    }


def get_target_file_name(text_path, file_path):
    return os.path.join(text_path, file_path) + ".json"


def get_file_desc(arc_base_dir, file_path):
    # TODO: optimise fio
    fstat = os.stat(file_path)
    is_ext_text, mime_type = unstruct_part.is_extract_mime_type(file_path)

    return file_desc_dict(
        arc_base_dir, file_path, fstat, is_ext_text, mime_type)


def get_save_dir_path(file_path, text_path):
    file_path_sep = file_path.rsplit(os.path.sep, 1)
    path_prefix, file_name = ("", file_path_sep[0]) if len(file_path_sep) == 1 else file_path_sep

    file_flat_name = get_flat_filename(file_name)

    return get_target_file_name(
        text_path,
        os.path.join(path_prefix, file_flat_name)
    )


def save_file_meta(
        text_path,
        file_path,
        file_desc,
        file_meta,
        file_text=""):
    json_data = file_desc | file_meta

    if file_text:
        json_data["text"] = file_text

    json_data['created_at'] = datetime.now().isoformat()

    save_dir_path = get_save_dir_path(file_path, text_path)

    os.makedirs(os.path.dirname(save_dir_path), exist_ok=True)
    with open(save_dir_path, "w") as fp:
        json.dump(json_data, fp)


def save_file_text(
        stats,
        arc_path,
        text_path,
        file_path,
        file_desc,
        text_meta,
        file_text):
    file_rel_path = file_path.removeprefix(arc_path)
    if "error_msg" in text_meta:
        stats["error_cnt"] += 1
        text_meta["file_rel_path"] = file_rel_path
        logger.error(text_meta)
        return

    if file_text:
        save_file_meta(
            text_path, file_rel_path, file_desc, text_meta, file_text)
        stats["text_extracted_cnt"] += 1
    else:
        stats["no_text_extracted_cnt"] += 1


def get_dir_stats_name(text_path, arc_path, root_dir):
    file_rel_dir = root_dir.removeprefix(arc_path)
    get_target_file_name(text_path, file_rel_dir)

    return os.path.join(file_rel_dir, "_stats")


def save_dir_meta(stats, arc_path, root_dir, text_path, sub_dir, files):
    # temporary for huge arc
    if arc_path != root_dir:
        stats_file_name = get_dir_stats_name(text_path, arc_path, root_dir)

        if os.path.isfile(get_target_file_name(text_path, stats_file_name)):
            stats["target_dir_exists"] += 1
            return False

    file_rel_dir = root_dir.removeprefix(arc_path)
    sub_dir_cnt = len(sub_dir)
    files_cnt = len(files)
    save_file_meta(
        text_path,
        os.path.join(file_rel_dir, "_stats"),
        {"file_rel_dir": file_rel_dir},
        {"sub_dir_cnt": sub_dir_cnt, "files_cnt": files_cnt}
    )

    stats["sub_dir_cnt"] += sub_dir_cnt
    stats["files_cnt"] += files_cnt
    return True


def analyse_arc_file(arc_path, text_path, root_dir, file_name, stats):
    file_path = os.path.join(root_dir, file_name)
    # TODO: should be parametrized, some info can be skipped
    if os.path.isfile(get_target_file_name(text_path, file_path)):
        stats["target_exists"] += 1
        return

    file_ext = file_name.rsplit(".", 1)[-1].lower()
    if file_ext not in cons_cleansing.TYPE_EXTRACT_EXT_SET:
        stats["skipped_by_extension"] += 1
        return

    logger.info("Analyse file %s", file_path)

    file_desc = get_file_desc(arc_path, file_path)
    # TODO: use heuristics to handle big files
    if file_desc["extract_text"]:
        if file_desc["file_size_kb"] > cons_cleansing.UNS_FILE_SIZE_MAX_KB:
            logger.info("File %s size > %s KB, skip", file_path, cons_cleansing.UNS_FILE_SIZE_MAX_KB)
            stats["skip_big_file_cnt"] += 1
            return

        text_meta, file_text = extract_text(file_path)
        stats["extract_text_cnt"] += 1
    else:
        stats["no_text_type_cnt"] += 1
        return

    save_file_text(
        stats,
        arc_path,
        text_path,
        file_path,
        file_desc,
        text_meta,
        file_text)
