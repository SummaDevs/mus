import time
from collections.abc import Iterator
from threading import Lock

import requests

DOWNLOAD_CHUNK_SIZE = 4096


class ThreadRateLimiter(Iterator):
    def __init__(self, interval):
        self.lock = Lock()
        self.interval = interval
        self.next_yield = 0

    def __next__(self):
        with self.lock:
            curr_time = time.time()
            if curr_time < self.next_yield:
                time.sleep(self.next_yield - curr_time)
                curr_time = time.time()
            self.next_yield = curr_time + self.interval


def download_url(url, save_path, chunk_size=DOWNLOAD_CHUNK_SIZE):
    res = requests.get(url, stream=True)
    if res.status_code == requests.codes.ok:
        with open(save_path, 'wb') as fd:
            for chunk in res.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
    return res.status_code
