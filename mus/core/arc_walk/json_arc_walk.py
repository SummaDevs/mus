import json
import logging
import os

from mus.config.config import app_config
from mus.constant.cons_cleansing import ES_DOC_EXT
from mus.constant.cons_cleansing import SKIP_JSON_FILE_SET
from mus.core.arc_walk.arc_walk import check_progress

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def json_file_iter(text_path, stats):
    for root_dir, sub_dir, files in os.walk(text_path):

        if not files:
            continue

        for file_name in files:
            if not check_progress("cnt", root_dir, file_name, stats):
                break

            _, short_name = os.path.split(file_name)
            if short_name in SKIP_JSON_FILE_SET:
                stats["skip_file_cnt"] += 1
                continue
            if not short_name.endswith(ES_DOC_EXT):
                stats["skip_file_ext_cnt"] += 1
                continue

            yield root_dir, file_name


def json_data_iter(text_path, lang_list, stats, file_max_cnt=None):
    for root_dir, file_name in json_file_iter(text_path, stats):
        if not check_progress("cnt", root_dir, file_name, stats, file_max_cnt=file_max_cnt):
            break

        file_path = os.path.join(root_dir, file_name)
        try:
            with open(file_path, "r") as fp:
                json_doc = json.load(fp)
        except json.JSONDecodeError:
            stats["json_error"] += 1
            continue

        if json_doc["lang"][0] in lang_list:
            yield file_path, json_doc


def update_json_file(text_path, update_json_func, file_items, stats, **kwargs):
    for idx, file_path in file_items:
        if not check_progress("updated_meta", text_path, file_path, stats):
            break

        json_path = os.path.join(text_path, file_path)

        with open(json_path, "r") as fpr:
            json_doc = json.load(fpr)

        update_json_func(idx, json_doc, **kwargs)

        with open(json_path, "w") as fpw:
            json.dump(json_doc, fpw)
