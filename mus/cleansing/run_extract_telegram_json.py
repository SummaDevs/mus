import json
import logging
import os
from collections import defaultdict
from copy import deepcopy

from mus.config.config import app_config
from mus.constant import cons_cleansing
from mus.core.file_utils.file_utils import get_file_desc
from mus.core.file_utils.path_utils import get_norm_file_name
from mus.core.lang.detect_utils import detect_language
from mus.data_models.json_doc_models.es_json_text_upd import update_json_telegram

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def get_tel_mes_file_name(message):
    return "-".join((message["date"].replace(":", "-"), str(message["id"]))) + ".json"


def get_message_text(message):
    txt = ""

    text = message.get("text")
    text_entities = message.get("text_entities")
    if text and isinstance(text, str):
        txt = text
    elif text and isinstance(text, list):
        txt = "\n".join(
            (part if isinstance(part, str) else part.get("text", "") for part in text)
        )
    if text_entities and isinstance(text_entities, list):
        txt = "\n".join(
            (ent if isinstance(ent, str) else ent.get("text", "") for ent in text_entities)
        )

    return txt


def get_tel_data(file_full_name):
    logger.info("Analyse file %s", file_full_name)

    with open(file_full_name, "r") as fp:
        json_doc = json.load(fp)

    return json_doc


def get_collection_desc(arc_path, file_full_name):
    file_ext = file_full_name.rsplit(".", 1)[-1].lower()

    return get_file_desc(arc_path, file_full_name, file_ext)


def process_text(file_desc_dict, mes, current_subdir, file_path, text, stats):
    text_lang = detect_language(text)
    lang = text_lang[0]["lang"]

    if lang not in cons_cleansing.WORKING_LANGUAGES:
        stats[f"unsupported_lang_{lang}"] += 1
        return

    json_doc = deepcopy(file_desc_dict)

    file_name = get_tel_mes_file_name(mes)
    file_full_name = os.path.join(current_subdir, file_name)

    update_json_telegram(
        mes["id"],
        json_doc,
        mes=mes,
        file_path=os.path.join(file_path, file_name),
        text=text,
        lang=[lang]
    )

    with open(file_full_name, "w") as fpw:
        json.dump(json_doc, fpw)

    stats["message_saved"] += 1


def process_messages(text_path, collection_name, json_doc, file_desc_dict, stats):
    message_day = None
    current_subdir = None

    for mes in json_doc["messages"]:
        if mes.get("type", "") == "message":
            stats["message_cnt"] += 1

            # create_day_subdir
            mes_day = mes["date"][:10]
            if message_day != mes_day:
                message_day = mes_day

                current_subdir = os.path.join(text_path, collection_name, message_day)

                os.makedirs(current_subdir, exist_ok=True)

            text = get_message_text(mes)
            if text:
                process_text(
                    file_desc_dict,
                    mes,
                    current_subdir,
                    os.path.join(collection_name, message_day),
                    text,
                    stats
                )

            else:
                stats["non_text_cnt"] += 1
        else:
            stats["non_message_cnt"] += 1


def process_json_file(arc_path, text_path, tg_json_file, stats):
    file_full_name = os.path.join(arc_path, tg_json_file)

    json_doc = get_tel_data(file_full_name)

    file_desc_dict = get_collection_desc(arc_path, file_full_name)

    collection_name = get_norm_file_name(json_doc["name"])

    process_messages(text_path, collection_name, json_doc, file_desc_dict, stats)


def run_extract_telegram_json(_, arc_path, text_path, tg_json_file="result.json"):
    logger.info("Start processing %s/%s", arc_path, tg_json_file)

    stats = defaultdict(int)

    process_json_file(arc_path, text_path, tg_json_file, stats)

    logger.info(stats)
    logger.info("Exit processing")
