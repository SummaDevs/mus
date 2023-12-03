from collections import defaultdict

import spacy

from mus.constant import cons_nlp


class NLP:

    def __init__(self):
        self.nlp = defaultdict(dict)
        self.nlp_loaders = {
            "spacy": self._spacy_load
        }

    @staticmethod
    def _spacy_load(lang, **kwargs):
        return spacy.load(f"{lang}_core_news_lg", **kwargs)

    def load(self, lib_name, *lang_list, **kwargs):

        for lang in lang_list:
            if lang in cons_nlp.NLP_LANG and lib_name in self.nlp_loaders:
                if lang not in self.nlp[lib_name]:
                    self.nlp[lib_name][lang] = self.nlp_loaders[lib_name](lang, **kwargs)
            else:
                raise NotImplemented(
                    "%s language analysis is not implemented, please use: %s", lang, ",".join(cons_nlp.NLP_LANG))

        return self

    def __call__(self, *args, **kwargs):
        """
        Signature:
        nlp = NLP("spacy", "en", "ru")
        nlp(lib_name="spacy", lang="en", text="once upon a time")

        :param args: are not expected
        :param kwargs: dict
            lib_name="spacy",
            lang="en",
            text="once upon a time"
        :return:
        """
        return self.nlp[kwargs["lib_name"]][kwargs["lang"]](kwargs["text"])


nlp = NLP()
