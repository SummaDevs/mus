from mus.core.text.text_utils import get_doc_lines
from mus.nlp.nlp_loader import nlp


def get_text_tokens(nlp_lib, lang, analyse_func, text):
    tokens = []

    for text_line in get_doc_lines(text):
        doc = nlp(lib_name=nlp_lib, lang=lang, text=text_line)
        analyse_func(doc, tokens)

    return tokens
