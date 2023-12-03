import json
import os

from mus.data_models.es_models.arc_text_model import ArcText


def check_es_index(is_create_index, logger):
    es_arc_doc = ArcText()
    es_index_name = es_arc_doc.Index.name

    if is_create_index:
        logger.info("Drop and create index %s", es_index_name)
        ArcText.init()

    return es_index_name


def get_arc_doc_props():
    return ArcText().get_mapping()["arc_text"]["mappings"]["properties"]


def index_file(root_dir, file_name, arc_doc_att, stats):
    file_path = os.path.join(root_dir, file_name)

    try:
        with open(file_path, "r") as fp:
            json_doc = json.load(fp)
    except json.JSONDecodeError:
        stats["json_decode_error"] += 1
        return

    es_arc_doc = ArcText(meta={'id': json_doc["file_path"]})

    for att, val in json_doc.items():
        if att in arc_doc_att:
            setattr(es_arc_doc, att, val)

    es_arc_doc.save()
    stats["arc_files_indexed"] += 1
