from hashlib import blake2b
from textwrap import TextWrapper

from mus.constant import cons_nlp

text_wrapper = TextWrapper(
    width=cons_nlp.LINE_PIPE_LEN,
    initial_indent="",
    subsequent_indent="",
    expand_tabs=True,
    replace_whitespace=True,
    fix_sentence_endings=True,
    break_long_words=False,
    drop_whitespace=True,
    break_on_hyphens=False,
    tabsize=2,
)


def get_digest_int(text):
    return int(blake2b(text.encode(), digest_size=2).hexdigest(), 16)


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
