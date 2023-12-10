import json
import os
from threading import Lock

from mus.constant.cons_gdelt20 import GDELT_LANGUAGE
from mus.gdelt20.common import gd_path_gen

KEY_SUF_CNT = "_cnt"
KEY_SUF_DATE = "_dt"

CHECK_POINT_NUM = 100


class Gdelt20CheckPoint():
    def __init__(self, base_path, finish_date, start_date):
        self._lock = Lock()

        self.language = self.language_cnt = self.language_dt = None
        self.set_language(GDELT_LANGUAGE[0])

        self.path_gen = gd_path_gen.Gdelt20PathGen(base_path, finish_date, start_date)

        self._checkpoint_dict = self._get_checkpoint_init_dict()

        self.checkpoint_file_name = self.path_gen.get_checkpoint_file_name()
        self._init_checkpoint()

    def __str__(self):
        return str(self._checkpoint_dict)

    def _get_checkpoint_init_dict(self):
        cp_dict = {
            "base_path": self.path_gen.base_path,
            "start_date": int(self.path_gen.start_date_str),
            "finish_date": int(self.path_gen.finish_date_str),
        }
        cp_dict.update(
            {file_type + cnt_type: 0
             for file_type in GDELT_LANGUAGE
             for cnt_type in (KEY_SUF_CNT, KEY_SUF_DATE)}
        )
        return cp_dict

    def _init_checkpoint(self):
        with self._lock:
            if os.path.isfile(self.checkpoint_file_name):
                with open(self.checkpoint_file_name) as cpf:
                    self._checkpoint_dict = json.load(cpf)
            else:
                self._checkpoint()

    def _checkpoint(self):
        with open(self.checkpoint_file_name, "w") as cpf:
            json.dump(self._checkpoint_dict, cpf)

    def set_language(self, language):
        if language in GDELT_LANGUAGE:
            self.language = language
            self.language_cnt = self.language + KEY_SUF_CNT
            self.language_dt = self.language + KEY_SUF_DATE
        else:
            raise NotImplementedError(f"Language {language} is not implemented")

    def get_cnt(self):
        with self._lock:
            return self._checkpoint_dict[self.language_cnt]

    def update_checkpoint(self, dt):
        with self._lock:
            self._checkpoint_dict[self.language_cnt] += 1
            self._checkpoint_dict[self.language_dt] = dt
            if not self._checkpoint_dict[self.language_cnt] % CHECK_POINT_NUM:
                self._checkpoint()
