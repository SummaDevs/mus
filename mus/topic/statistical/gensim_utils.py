import pyLDAvis
import pyLDAvis.gensim_models
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore

from mus.constant import cons_nlp
from mus.constant import cons_topic
from mus.constant import constant
from mus.core.arc_walk.json_arc_walk import json_data_iter
from mus.core.text import text_utils
from mus.nlp.nlp_token import get_text_tokens


def get_tokens(doc, tokens):
    for tok in doc:
        lemma = tok.lemma_.lower()
        if (lemma not in cons_nlp.REMOVE_TOKENS and
                len(lemma) >= cons_nlp.TOK_FILTER_MIN_LEN and
                tok.pos_ not in cons_nlp.MINOR_TOKENS_SET and not
                tok.is_stop and tok.is_alpha):
            tokens.append(lemma)

    return tokens


def get_gens_corpus(text_path, nlp_lib, lang_list, stats):
    # TODO: parallel, not in mem
    file_tokens = []
    file_map = {}

    for idx, (file_path, json_doc) in enumerate(
            json_data_iter(text_path, lang_list, stats, cons_topic.FILE_MAX_CNT)):

        tokens = get_text_tokens(nlp_lib, json_doc["lang"][0], get_tokens, json_doc["text"])

        if tokens:
            file_tokens.append(tokens)
            file_map[idx] = file_path.removeprefix(text_path)

    gens_dict = Dictionary(file_tokens)
    gens_dict.filter_extremes(
        no_below=cons_topic.TOK_FILTER_NO_BELOW_DOC,
        no_above=cons_topic.TOK_FILTER_NO_ABOVE,
        keep_n=cons_topic.TOK_FILTER_KEEP_N,
        keep_tokens=cons_topic.TOK_FILTER_KEEP_TOKENS
    )

    corpus = [gens_dict.doc2bow(tok) for tok in file_tokens]

    return gens_dict, corpus, file_map


def get_lda_model(corpus, gens_doc):
    lda_model = LdaMulticore(
        corpus=corpus,
        id2word=gens_doc,
        num_topics=cons_topic.LDA_NUM_TOPICS,
        iterations=cons_topic.LDA_ITERATIONS,
        workers=constant.CPU_CORES,
        passes=cons_topic.LDA_PASSES
    )
    return lda_model


def save_lda_vis(lda_model, corpus, gens_dict, result_vis_file):
    lda_viz = pyLDAvis.gensim_models.prepare(
        lda_model, corpus, gens_dict, mds='mmds')

    pyLDAvis.save_html(lda_viz, result_vis_file)


def get_topics_words(lda_model):
    topics_dict = {}
    for num, topic in lda_model.print_topics(num_topics=cons_topic.LDA_NUM_TOPICS, num_words=cons_topic.LDA_NUM_WORDS):
        topic_words = [ts.split("*")[1] for ts in topic.replace('"', "").split(" + ")]
        topics_dict[num] = {
            "topic_num": text_utils.get_digest_int(",".join(topic_words)),
            "topic_words": topic_words
        }
    return topics_dict
