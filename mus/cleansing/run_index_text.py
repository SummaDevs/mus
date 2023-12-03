import logging
from collections import defaultdict

from mus.cleansing.arc_walk.jsonarc_walk import arc_walk_iter
from mus.config.config import app_config
from mus.core.es.es_arc_index_file import check_es_index
from mus.core.es.es_arc_index_file import get_arc_doc_props
from mus.core.es.es_arc_index_file import index_file
from mus.core.es.es_conn import create_es_conn

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def run_index_text(config_obj, text_path, is_create_index):
    create_es_conn(config_obj)

    es_index_name = check_es_index(is_create_index, logger)

    logger.info("Start walking in %s, index %s", text_path, es_index_name)

    stats = defaultdict(int)

    arc_doc_att = set(get_arc_doc_props().keys())
    for root_dir, file_name in arc_walk_iter(text_path, stats):
        index_file(root_dir, file_name, arc_doc_att, stats)

    logger.info(stats)
    logger.info("Exit walk")
