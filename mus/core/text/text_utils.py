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
