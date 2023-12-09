from elasticsearch_dsl import analyzer
from elasticsearch_dsl import token_filter

en_stop = token_filter('en_stop', type="stop", stopwords="_english_")
en_stemmer = token_filter('en_stemmer', type="stemmer", language="english")
ru_stop = token_filter('ru_stop', type="stop", stopwords="_russian_")
ru_stemmer = token_filter('ru_stemmer', type="stemmer", language="russian")

# requires locale setup
ru_hunspell = token_filter('ru_hunspell', type="hunspell", locale="ru_RU", dedup=False)

en_ru_analyzer = analyzer(
    'en_ru_analyzer',
    tokenizer='lowercase',
    filter=[
        'lowercase',
        ru_stop,
        ru_stemmer,
        en_stop,
        en_stemmer,
    ]
)
