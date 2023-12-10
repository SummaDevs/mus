from mus.gdelt20.common import request_utils
from mus.constant import cons_gdelt20_api


class Gdelt20ApiClietnt():
    def __init__(self):
        self.rate_limiter = request_utils.ThreadRateLimiter(cons_gdelt20_api.API_RATE_LIMIT)

    def save_file_list(self, language, save_path):
        url = cons_gdelt20_api.API_MASTER_FILE_LIST_URL[language]
        next(self.rate_limiter)

        return request_utils.download_url(url, save_path)

    def save_file(self, language, ts, obj_type, save_path):
        url = cons_gdelt20_api.API_FILE_LIST_URL[language][obj_type].format(ts, obj_type)

        next(self.rate_limiter)
        return request_utils.download_url(url, save_path), url


gd_api_client = Gdelt20ApiClietnt()
