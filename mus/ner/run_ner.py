import logging
from collections import defaultdict

from mus.config.config import app_config
from mus.constant import cons_ner
from mus.constant import cons_nlp
from mus.core.arc_walk.json_arc_walk import json_data_iter
from mus.core.arc_walk.json_arc_walk import update_json_file
from mus.data_models.json_doc_models.es_json_text_upd import update_json_ner
from mus.nlp.nlp_loader import nlp
from mus.nlp.nlp_token import get_text_tokens

logger = logging.getLogger(name=app_config["PROJECT_NAME"])


def get_named_entities(doc, tokens):
    for tok in doc:
        if tok.ent_type_ and tok.ent_type_ not in cons_ner.EXCLUDE_NE_TYPE:
            lemma = tok.lemma_.lower()
            if lemma not in cons_nlp.REMOVE_TOKENS and len(lemma) >= cons_nlp.TOK_FILTER_MIN_LEN:
                tokens.append({
                    "ne_id": tok.ent_id_,
                    "ne_name": lemma,
                    "ne_type": tok.ent_type_,
                })

    return tokens


def run_dir_ner(text_path, nlp_lib, lang_list, update, stats):
    for idx, (file_path, json_doc) in enumerate(json_data_iter(text_path, lang_list, stats)):

        named_entities = get_text_tokens(nlp_lib, json_doc["lang"][0], get_named_entities, json_doc["text"])

        if update:
            update_json_file(
                text_path,
                update_json_ner,
                [(idx, file_path)],
                stats,
                named_entities=named_entities
            )
        else:
            logger.info({"file_path": file_path, "named_entities": named_entities})


def run_ner(_, text_path, lang_list, update, nlp_lib=cons_ner.DEFAULT_NLP):
    stats = defaultdict(int)

    logger.info(
        "Start walking in %s, languages %s, update %s",
        text_path, ",".join(lang_list), update
    )

    logger.info(f"Loading {nlp_lib} models")
    # TODO: add_pipe=["entity_linker"] and create model
    nlp.load(nlp_lib, *lang_list)

    run_dir_ner(text_path, nlp_lib, lang_list, update, stats)

    logger.info(stats)

    logger.info("Finish NER")
