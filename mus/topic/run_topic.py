import json
import logging
import os
from collections import defaultdict

from mus.config.config import app_config
from mus.constant import cons_topic
from mus.core.file_utils.path_utils import norm_dir_path
from mus.nlp.nlp_loader import nlp
from mus.topic.statistical import gensim_utils

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def update_json_doc(lda_model, corpus, idx, json_doc, topics_words_list):
    num = lda_model[corpus][idx][0][0]
    json_doc["topics"] = topics_words_list[num]["topic_words"]
    json_doc["topics_num"] = topics_words_list[num]["topic_num"]


def update_files_topics(text_path, lda_model, corpus, file_map, stats):
    topics_words_list = gensim_utils.get_topics_words(lda_model)

    for idx, file_meta in file_map.items():

        json_path = os.path.join(text_path, file_meta["file_path"])

        with open(json_path, "r") as fpr:
            json_doc = json.load(fpr)

        update_json_doc(lda_model, corpus, idx, json_doc, topics_words_list)

        with open(json_path, "w") as fpw:
            json.dump(json_doc, fpw)

        stats["updated_meta"] += 1

        if not stats["updated_meta"] % cons_topic.LOG_FILE_CNT:
            logger.info(stats)
            logger.info("Last file %s", json_path)


def run_dir_topic(text_path, nlp_lib, lang_list, update, stats):
    logger.info("Loading gensim dictionary, source %s", text_path)
    gens_dict, corpus, file_map = gensim_utils.get_gens_corpus(text_path, nlp_lib, lang_list, stats)

    if gens_dict.num_docs and corpus[0]:
        logger.info("Training LDA model, source %s", text_path)
        lda_model = gensim_utils.get_lda_model(corpus, gens_dict)
    else:
        logger.info("Json data does not found, source %s", text_path)
        return

    result_vis_file = os.path.join(text_path, cons_topic.FILE_TOPICS_VIZ_NAME)
    logger.info("Saving topic visualisation into %s", result_vis_file)
    gensim_utils.save_lda_vis(lda_model, corpus, gens_dict, result_vis_file)

    if update:
        logger.info("Updating topics, source %s", text_path)
        update_files_topics(text_path, lda_model, corpus, file_map, stats)


def run_model_topic(_, text_path, lang_list, per_subdir, update, nlp_lib=cons_topic.DEFAULT_NLP):
    stats = defaultdict(int)

    logger.info(
        "Start walking in %s, per sub-directories %s, languages %s using %s",
        text_path,
        per_subdir,
        ",".join(lang_list),
        nlp_lib
    )

    logger.info(f"Loading {nlp_lib} models")
    nlp.load(nlp_lib, *lang_list)  # , exclude=["ner"]

    if per_subdir:
        subdir_list = [
            norm_dir_path(os.path.join(text_path, obj)) for obj in os.listdir(text_path)
            if os.path.isdir(os.path.join(text_path, obj))
        ]
        for dir_name in subdir_list:
            run_dir_topic(dir_name, nlp_lib, lang_list, update, stats)

    else:
        run_dir_topic(text_path, nlp_lib, lang_list, update, stats)

    logger.info(stats)
