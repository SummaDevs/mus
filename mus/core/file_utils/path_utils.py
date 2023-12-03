import os


def norm_dir_path(dir_path):
    return dir_path if dir_path.endswith(os.path.sep) else f"{dir_path}{os.path.sep}"
