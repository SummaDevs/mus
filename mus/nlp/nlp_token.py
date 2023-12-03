from mus.constant import cons_nlp
from mus.core.text.text_utils import text_wrapper
from mus.nlp.nlp_loader import nlp


def get_wrapped_line(text_line, text_len):
    wrapped_line = text_wrapper.wrap(text_line)

    for line in wrapped_line:
        line_len = len(line)

        if line_len < cons_nlp.LINE_TEXT_MIN_LEN:
            continue

        text_len += line_len
        if text_len <= cons_nlp.TEXT_MAX_LEN:
            return line, text_len
        else:
            break

    return "", text_len


def get_doc_lines(text):
    text_len = 0
    for text_line in text.splitlines():
        line, text_len = get_wrapped_line(text_line, text_len)
        if text_len <= cons_nlp.TEXT_MAX_LEN:
            if line:
                yield line
        else:
            break


def analyse_tokens(nlp_lib, lang, text_line, clean_tokens):
    doc = nlp(lib_name=nlp_lib, lang=lang, text=text_line)
    for tok in doc:
        lemma = tok.lemma_.lower()
        if (lemma not in cons_nlp.REMOVE_TOKENS and
                len(lemma) >= cons_nlp.TOK_FILTER_MIN_LEN and
                tok.pos_ not in cons_nlp.MINOR_TOKENS_SET and not
                tok.is_stop and tok.is_alpha):
            clean_tokens.append(lemma)

    return clean_tokens


def get_tokens(nlp_lib, lang, text):
    clean_tokens = []

    for text_line in get_doc_lines(text):
        analyse_tokens(nlp_lib, lang, text_line, clean_tokens)

    return clean_tokens
