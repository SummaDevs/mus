import logging
from collections import defaultdict

from mus.config.config import app_config

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def run_ner(_, text_path, lang_list, update):
    stats = defaultdict(int)

    logger.info(
        "Start walking in %s, languages %s, update %s",
        text_path,
        ",".join(lang_list),
        update
    )

    logger.info("Loading spicy models")

    logger.info(stats)
