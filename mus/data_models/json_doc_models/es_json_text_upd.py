from datetime import datetime

from mus.constant import cons_topic
from mus.constant import constant

"""

Note: the fields naming should be according to the es_json_text_model.ArcDoc

"""


def ts_to_utc(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def file_desc_dict(collection, file_path, fstat, file_ext, is_ext_text, mime_type):
    return {
        "collection": collection,
        "file_path": file_path,
        "file_extension": file_ext,
        "extract_text": is_ext_text,
        "file_mime_type": mime_type,
        "file_size_kb": fstat.st_size // constant.K_BYTE,
        "datetime_access": ts_to_utc(fstat.st_atime),
        "datetime_modification": ts_to_utc(fstat.st_mtime),
        "datetime_meta": ts_to_utc(fstat.st_ctime),
        "text": "",
        "created_at": datetime.now().isoformat(),
    }


def update_json_top(idx, json_doc, lda_model=None, corpus=None, topics_words_list=None):
    try:
        doc_idx = lda_model[corpus][idx]
        num = doc_idx[0][0]
        json_doc["topics"] = topics_words_list[num]["topic_words"]
        json_doc["topics_num"] = topics_words_list[num]["topic_num"]
    except IndexError:
        # empty doc? clarify
        json_doc["topics"] = []
        json_doc["topics_num"] = cons_topic.UNKNOWN_TOPIC_NUM


def update_json_ner(_, json_doc, named_entities=None):
    json_doc["named_entities"] = named_entities


def update_json_telegram(_, json_doc, mes=None, file_path=None, text=None, lang=None):
    json_doc["file_path"] = file_path
    json_doc["extract_text"] = bool(mes["text"])
    json_doc["datetime_meta"] = mes["date"]

    json_doc["file_mime_type"] = mes.get("mime_type", "")

    json_doc["data_origin"] = mes.get("forwarded_from", 0)
    json_doc["media_file"] = mes.get("file", 0)
    json_doc["duration_seconds"] = mes.get("duration_seconds", 0)
    json_doc["width"] = mes.get("width", 0)
    json_doc["height"] = mes.get("height", 0)

    json_doc["text"] = text
    json_doc["lang"] = lang
