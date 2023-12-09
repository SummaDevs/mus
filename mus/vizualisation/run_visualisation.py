import json
import logging
import os
from collections import defaultdict
from traceback import print_exc

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from mus.core.arc_walk.json_arc_walk import json_file_iter
from mus.config.config import app_config
from mus.constant import cons_ner

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


# TODO: refactor using NER / terminology extractor

def add_topic_ne_text(json_doc, topics_names, topics_text):
    if isinstance(json_doc, dict) and "named_entities" in json_doc:
        named_entities = json_doc.get("named_entities") or []
        topic_num = json_doc.get("topics_num") or 0
        if topic_num not in topics_names:
            if topic_num:
                topics_names[topic_num] = ",".join(sorted(json_doc.get("topics", ["No name"])))
            else:
                topics_names[topic_num] = "Zero name"

        topics_text[topic_num] += " " + " ".join(
            # f"{ne['ne_name']}_{ne['ne_type']}"
            (ne['ne_name'] for ne in named_entities if ne['ne_type'] not in cons_ner.EXCLUDE_NE_TYPE))


def agg_named_entities(root_dir, file_name, topics_names, topics_text, stats):
    full_path = os.path.join(root_dir, file_name)

    try:
        with open(full_path, "r") as fpr:
            json_doc = json.load(fpr)
        stats["json_reads"] += 1

    except json.JSONDecodeError:

        stats["json_decode_error"] += 1
        print_exc()
        return

    add_topic_ne_text(json_doc, topics_names, topics_text)


def visualize_text(fig_file_name, text, title):
    wordcloud = WordCloud(
        width=1920,
        height=1080,
        background_color='white',
        max_words=200
    ).generate(text)

    # Plot the WordCloud
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    plt.title(f'Source: {title}', loc="center", fontsize=14)
    plt.savefig(fig_file_name, format="png")


def run_wordcloud_viz(_, text_path, per_subdir, per_topic):
    logger.info("Start walking in %s, per subdir %s", text_path, per_subdir)

    stats = defaultdict(int)

    topics_text = defaultdict(str)
    topics_names = {}

    for root_dir, file_name in json_file_iter(text_path, stats):
        agg_named_entities(root_dir, file_name, topics_names, topics_text, stats)

    if per_topic:
        pass
    else:
        text = " ".join((txt for txt in topics_text.values()))
        fig_file_name = os.path.join(text_path, "wordcloud.png")
        visualize_text(fig_file_name, text, f"all topics {text_path}")

    logger.info(stats)
    logger.info("Finish")
