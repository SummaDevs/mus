"""
gdelt20 API constants
"""

API_RATE_LIMIT = 0.25  # 4 request/sec

DATA_CHUNK_SIZE = 4096

API_ERROR_MAX = 100

API_BASE_URL = "http://data.gdeltproject.org/gdeltv2"

API_MASTER_FILE_LIST_URL = {
    "en": API_BASE_URL + "/masterfilelist.txt",
    "tl": API_BASE_URL + "/masterfilelist-translation.txt"
}

API_FILE_LIST_URL = {
    "en": {
        "export": API_BASE_URL + "/{}.{}.CSV.zip",
        "mentions": API_BASE_URL + "/{}.{}.CSV.zip",
        "gkg": API_BASE_URL + "/{}.{}.csv.zip"
    },
    "tl": {
        "export": API_BASE_URL + "/{}.translation.{}.CSV.zip",
        "mentions": API_BASE_URL + "/{}.translation.{}.CSV.zip",
        "gkg": API_BASE_URL + "/{}.translation.{}.csv.zip"
    }
}
