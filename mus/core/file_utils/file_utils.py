import os
from hashlib import blake2b

FILE_PATH_MAX_LEN = 1028
FILE_NAME_MAX_LEN = 255
HEX_DIGEST_SIZE = 16
# todo: handle utf8 precisely
FILE_SUB_LEN = FILE_NAME_MAX_LEN // 2 - HEX_DIGEST_SIZE + 1


def get_hexdigest(text, digest_size=HEX_DIGEST_SIZE):
    return blake2b(text.encode(), digest_size=digest_size).hexdigest()


def get_flat_filename(file_name, extension=""):
    if extension:
        file_name += extension
    std_file_name = file_name.replace(os.path.sep, "-")

    std_file_name = std_file_name if len(std_file_name.encode('utf-8')) <= FILE_NAME_MAX_LEN else (
            std_file_name[:-FILE_SUB_LEN] + "-" + get_hexdigest(std_file_name))

    return std_file_name
