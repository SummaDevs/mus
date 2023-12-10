import datetime
import os

from dateutil.relativedelta import relativedelta

from mus.gdelt20.common import gd_path_gen


def get_target_path_list(base_path, start_date, finish_date, language, obj_type, obj_format):
    path_gen = gd_path_gen.Gdelt20PathGen(base_path, start_date, finish_date)

    yield path_gen.get_metadata_dir()

    partition_date = datetime.datetime(start_date.year, start_date.month, 1)

    while partition_date <= finish_date:
        yield path_gen.get_month_partition_dir(language, obj_type, obj_format, partition_date)
        partition_date += relativedelta(months=1)


def create_path_tree(base_path, start_date, finish_date, languages, obj_types):
    for language in languages:
        for obj_type in obj_types:
            for target_path in get_target_path_list(
                    base_path, start_date, finish_date, language, obj_type, gd_path_gen.GDELT_FILE_FORMAT):
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                assert os.path.isdir(target_path), f"Target path {target_path} is not a directory"
