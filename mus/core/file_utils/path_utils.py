import os

import re
from hashlib import blake2b

FILE_PATH_MAX_LEN = 1028
FILE_NAME_MAX_LEN = 255
HEX_DIGEST_SIZE = 16
# todo: handle utf8 precisely
FILE_SUB_LEN = FILE_NAME_MAX_LEN // 2 - HEX_DIGEST_SIZE + 1

RE_PATH_COMP = re.compile(r'[^\w_.-]')


def get_hexdigest(text, digest_size=HEX_DIGEST_SIZE):
    return blake2b(text.encode(), digest_size=digest_size).hexdigest()


def get_norm_file_name(file_name):
    return RE_PATH_COMP.sub('_', file_name)


def get_flat_filename(file_name, extension=""):
    if extension:
        file_name += extension
    std_file_name = get_norm_file_name(file_name)

    std_file_name = std_file_name if len(std_file_name.encode('utf-8')) <= FILE_NAME_MAX_LEN else (
            std_file_name[:-FILE_SUB_LEN] + "-" + get_hexdigest(std_file_name))

    return std_file_name


def get_target_full_name(text_path, file_path, file_extension=".json"):
    return os.path.join(text_path, file_path) + file_extension


def norm_dir_path(dir_path):
    return dir_path if dir_path.endswith(os.path.sep) else f"{dir_path}{os.path.sep}"


def get_dir_stats_name(text_path, arc_path, root_dir):
    file_rel_dir = root_dir.removeprefix(arc_path)
    get_target_full_name(text_path, file_rel_dir)

    return os.path.join(file_rel_dir, "_stats")


def get_save_dir_path(file_path, text_path):
    file_path_sep = file_path.rsplit(os.path.sep, 1)
    path_prefix, file_name = ("", file_path_sep[0]) if len(file_path_sep) == 1 else file_path_sep

    file_flat_name = get_flat_filename(file_name)

    return get_target_full_name(
        text_path,
        os.path.join(path_prefix, file_flat_name)
    )
