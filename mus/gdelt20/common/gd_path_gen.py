import os

from mus.constant.cons_gdelt20_api import API_MASTER_FILE_LIST_URL

GDELT_METADATA_DIR = 'metadata'
CHECK_POINT_FILE = 'check_point_{start_date}_{finish_date}.json'

GDELT_FILE_PREFIX_TPL = "\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}"
GDELT_FILE_PREFIX_DTPL = "%Y%m%d%H%M%S"
GDELT_FILE_FORMAT = 'tsv'

GDELT_FILE_SUF = ".{}.CSV.zip"

API_FILE_NAME_TMPL = {
    "en": "{}.{}.csv.zip",
    "tl": "{}.translation.{}.csv.zip"
}


class Gdelt20PathGen:
    def __init__(self, base_path, start_date, finish_date):
        self.base_path = base_path
        self.metadata_dir = os.path.join(self.base_path, GDELT_METADATA_DIR)

        self.start_date = start_date
        self.start_date_str = self.start_date.strftime(GDELT_FILE_PREFIX_DTPL)
        self.finish_date = finish_date
        self.finish_date_str = self.finish_date.strftime(GDELT_FILE_PREFIX_DTPL)

    def get_metadata_dir(self):
        return os.path.join(self.base_path, GDELT_METADATA_DIR)

    def get_month_partition_dir(self, language, obj_type, obj_format, partition_date):
        return os.path.join(
            self.base_path,
            language,
            obj_type,
            obj_format,
            partition_date.strftime("%Y"),
            partition_date.strftime("%m")
        )

    def get_checkpoint_file_name(self):
        return os.path.join(
            self.get_metadata_dir(),
            CHECK_POINT_FILE.format(start_date=self.start_date_str, finish_date=self.finish_date_str)
        )

    def get_list_file_name_parts(self, language):
        list_full_file_name = API_MASTER_FILE_LIST_URL[language].split("/")[-1]
        return list_full_file_name.split(".")

    def get_list_file_full_name(self, language):
        list_file_name, file_extension = self.get_list_file_name_parts(language)
        target_file_name = f"{list_file_name}-{self.finish_date_str}.{file_extension}"
        return os.path.join(self.get_metadata_dir(), target_file_name)

    def get_list_timestamps_file_name(self, language):
        list_file_name, _ = self.get_list_file_name_parts(language)
        target_file_name = f"{list_file_name}-{self.start_date_str}-{self.finish_date_str}.json"
        return os.path.join(self.get_metadata_dir(), target_file_name)

    def get_log_file_name(self):
        target_file_name = f"log-{self.start_date_str}-{self.finish_date_str}.txt"
        return os.path.join(self.get_metadata_dir(), target_file_name)

    def get_data_file_path(self, language, obj_type, ts):
        ts_str = str(ts)
        yesr_str = ts_str[0:4]
        month_str = ts_str[4:6]
        return os.path.join(
            self.base_path,
            language,
            obj_type,
            GDELT_FILE_FORMAT,
            yesr_str,
            month_str,
            API_FILE_NAME_TMPL[language].format(ts, obj_type)
        )
