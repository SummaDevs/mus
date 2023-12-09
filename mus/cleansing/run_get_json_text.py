import json
import logging
import os
from collections import defaultdict
from traceback import print_exc

from mus.config.config import app_config
from mus.core.arc_walk.json_arc_walk import json_file_iter
from mus.core.file_utils.path_utils import get_flat_filename

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def run_get_json_text(_, json_path, text_path):
    logger.info("Start walking in %s, target %s", json_path, text_path)

    stats = defaultdict(int)

    os.makedirs(text_path, exist_ok=True)

    for root_dir, file_name in json_file_iter(json_path, stats):
        file_path = os.path.join(root_dir, file_name)
        stats["cnt"] += 1

        try:
            with open(file_path, "r") as fpr:
                json_doc = json.load(fpr)
            stats["json_reads"] += 1

        except json.JSONDecodeError:

            stats["json_decode_error"] += 1
            print_exc()
            continue

        if isinstance(json_doc, dict) and "text" in json_doc:

            full_name = os.path.join(root_dir.removeprefix(json_path), file_name)
            target_full_name = os.path.join(text_path, get_flat_filename(full_name))

            text = json_doc["text"]

            with open(target_full_name, "w") as fpw:
                fpw.write(text)
            stats["text_writes"] += 1
        else:

            stats["json_wrong_format"] += 1

    logger.info(stats)
    logger.info("Exit walk")
