import logging
import os
from collections import defaultdict

from mus.config.config import app_config
from mus.constant import cons_topic
from mus.core.arc_walk.json_arc_walk import update_json_file
from mus.core.file_utils.path_utils import norm_dir_path
from mus.data_models.json_doc_models.es_json_text_upd import update_json_top
from mus.nlp.nlp_loader import nlp
from mus.topic.statistical import gensim_utils

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


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
        topics_words_list = gensim_utils.get_topics_words(lda_model)

        update_json_file(
            text_path,
            update_json_top,
            file_map.items(),
            stats,
            lda_model=lda_model,
            corpus=corpus,
            topics_words_list=topics_words_list
        )


def run_model_topic(_, text_path, lang_list, per_subdir, update, nlp_lib=cons_topic.DEFAULT_NLP):
    stats = defaultdict(int)

    logger.info(
        "Start walking in %s, per sub-directories %s, languages %s using %s",
        text_path, per_subdir, ",".join(lang_list), nlp_lib
    )

    logger.info(f"Loading {nlp_lib} models")
    nlp.load(nlp_lib, *lang_list, exclude=["ner"])

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
