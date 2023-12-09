import json
import os

from mus.cleansing.unstruct import unstruct_part
from mus.core.file_utils.path_utils import get_dir_stats_name
from mus.core.file_utils.path_utils import get_save_dir_path
from mus.core.file_utils.path_utils import get_target_full_name
from mus.data_models.json_doc_models.es_json_text_upd import file_desc_dict


def get_file_desc(arc_base_dir, file_path, file_ext):
    # TODO: optimise fio, decouple with unstruct
    fstat = os.stat(file_path)
    is_ext_text, mime_type = unstruct_part.is_extract_mime_type(file_path)

    return file_desc_dict(
        arc_base_dir.split(os.path.sep)[-2],
        file_path.removeprefix(arc_base_dir),
        fstat,
        file_ext,
        is_ext_text,
        mime_type
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

    save_dir_path = get_save_dir_path(file_path, text_path)

    # TODO: track current dir
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

    if file_text:
        save_file_meta(
            text_path,
            file_rel_path,
            file_desc,
            text_meta,
            file_text
        )
        stats["text_extracted_cnt"] += 1
    else:
        stats["no_text_extracted_cnt"] += 1


def save_dir_meta(stats, arc_path, root_dir, text_path, sub_dir, files):
    # temporary for huge arc
    if arc_path != root_dir:
        stats_file_name = get_dir_stats_name(text_path, arc_path, root_dir)

        if os.path.isfile(get_target_full_name(text_path, stats_file_name)):
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
