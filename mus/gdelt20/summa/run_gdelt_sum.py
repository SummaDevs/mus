import datetime
import logging
from collections import defaultdict

import openai
import pandas as pd

from mus.config.config import app_config
from mus.constant import cons_gdelt20
from mus.constant import cons_openai
from mus.core.client.urllib_text import extract_url_text
from mus.core.text.str_utils import cut_str_to_bytes
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import CAMEO_CODE_DESC
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import INTEREST_CODE_SET

logger = logging.getLogger(app_config["PROJECT_NAME"])

openai.api_key = app_config["OPENAI"]["OPENAI_API_KEY"]


def read_geo_data(file_path, stats):
    data = pd.read_csv(file_path, dtype={cons_gdelt20.EVENT_CODE_FIELD: str})
    stats["event_cnt"] = data.shape[0]

    data = data[data.EventCode.isin(INTEREST_CODE_SET)]
    stats["event_intel_cnt"] = data.shape[0]

    data.drop_duplicates(
        subset=[cons_gdelt20.SOURCE_URL_FIELD],
        keep="last",
        inplace=True,
        ignore_index=True
    )
    stats["event_source_cnt"] = data.shape[0]

    data[cons_gdelt20.LATITUDE_FIELD] = data[cons_gdelt20.LATITUDE_FIELD].fillna(0)
    data[cons_gdelt20.LONGTITUDE_FIELD] = data[cons_gdelt20.LONGTITUDE_FIELD].fillna(0)

    return data


def summarise(text):
    text_to_sum = cut_str_to_bytes(text, cons_openai.OAI_COMP_WIN_MAX_LEN)
    prompt = f"{text_to_sum}{cons_openai.OAI_COMP_TL_DR}"

    try:
        response = openai.Completion.create(
            model=cons_openai.OPENAI_MODEL,
            prompt=prompt,
            temperature=cons_openai.OAI_COMP_TEMPERATURE,
            max_tokens=cons_openai.OAI_COMP_MAX_TOCKEN,
            top_p=cons_openai.OAI_COMP_TOP_P,
            frequency_penalty=cons_openai.OAI_COMP_FREQUENCY_PENALTY,
            presence_penalty=cons_openai.OAI_COMP_PRESENCE_PENALTY
        )
    except Exception as exp:
        return str(exp)

    if response.choices:
        return response.choices[0].text
    else:
        return text[cons_openai.OAI_COMP_MAX_TOCKEN]


def save_summary(sfo, event_desc, summary, page_contents):
    idx = int(summary.startswith("\n") or summary.startswith(":"))

    if page_contents:
        text = f"- {event_desc}\n:: {summary[idx:]}\n"
    else:
        text = f"- {event_desc} ::{summary[idx:]}\n"

    print(text)
    sfo.write(text)
    sfo.flush()


def sum_record(sfo, row, stats):
    url = row[cons_gdelt20.SOURCE_URL_FIELD]

    event_desc = (f"{CAMEO_CODE_DESC[row[cons_gdelt20.EVENT_CODE_FIELD]]}:" +
                  f"{row[cons_gdelt20.LATITUDE_FIELD]},{row[cons_gdelt20.LONGTITUDE_FIELD]}:{url}")

    page_title, page_contents = extract_url_text(url, logger=logger)

    if page_contents:
        summary = summarise(f"{page_title}\n{page_contents}")
        stats["sum_cnt"] += 1
    else:
        summary = page_title
        stats["sum_title_cnt"] += 1

    save_summary(sfo, event_desc, summary, page_contents)


def gen_summary(data, file_path, stats):
    with open(file_path + ".summary.txt", "w") as sfo:

        sfo.write(f"{file_path}:{datetime.datetime.now()}, {stats}\n")

        for _, row in data.iterrows():

            sum_record(sfo, row, stats)

            if stats["sum_cnt"] >= cons_gdelt20.SUMMARY_MAX_REQ:
                break


def run_gdelt_sum(_, base_path):
    stats = defaultdict(int)

    logger.info("Reading gdelt data")
    data = read_geo_data(base_path, stats)

    logger.info("Summarise gdelt data")
    gen_summary(data, base_path, stats)
