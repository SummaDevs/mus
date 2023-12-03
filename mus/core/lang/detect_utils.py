from langdetect import LangDetectException
from langdetect import detect_langs


def detect_language(text):
    try:
        langs = detect_langs(text)

        return [{"lang": item.lang, "prob:": item.prob} for item in langs]

    except LangDetectException as _:
        return [{"lang": "err", "prob:": 0.0}]
