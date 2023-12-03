import logging
import sys
from collections import ChainMap
from copy import deepcopy

import urllib3


class HumanHTTPHandler(logging.Handler):
    """
    Normal HTTPHandler without overhead in standard header

    """

    _headers = {
        "Content-Type": "application/json"
    }

    def __init__(self, url, token=None):
        super(HumanHTTPHandler, self).__init__()
        self.url = url
        self.token = token

        # headers
        self.headers = self._headers
        if self.token:
            self.headers = ChainMap(deepcopy(self._headers), {"Authorization": self.token})

    def emit(self, record):
        """
        Send record use http

        :param record: app_logger record object
        :type record: LogRecord

        """

        try:

            urllib3.PoolManager().request(
                method="POST",
                url=self.url,
                headers=self.headers,
                body=self.format(record)
            )

        except Exception as e:
            sys.stderr.write(f"Logger HumanHTTPHandler fail with error: {e}")
            self.handleError(record)
