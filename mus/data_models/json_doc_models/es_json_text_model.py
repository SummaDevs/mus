from elasticsearch_dsl import Boolean
from elasticsearch_dsl import Date
from elasticsearch_dsl import Document
from elasticsearch_dsl import InnerDoc
from elasticsearch_dsl import Integer
from elasticsearch_dsl import Keyword
from elasticsearch_dsl import MetaField
from elasticsearch_dsl import Nested
from elasticsearch_dsl import Text

from mus.core.es.es_analysis import en_ru_analyzer

KEYWORD_MAX_LEN = 256

FIELD_DATA_FREQUENCY_FILTER = {
    "min": 0.01,
    "max": 0.2,
    "min_segment_size": 1024
}


class DataLineage(InnerDoc):
    proc_name = Keyword(ignore_above=KEYWORD_MAX_LEN)
    proc_type = Keyword(ignore_above=KEYWORD_MAX_LEN)
    proc_version = Keyword(ignore_above=KEYWORD_MAX_LEN)
    proc_date = Date()


class NamedEntity(InnerDoc):
    ne_id = Keyword(ignore_above=KEYWORD_MAX_LEN)
    ne_name = Keyword(ignore_above=KEYWORD_MAX_LEN)
    ne_type = Keyword(ignore_above=KEYWORD_MAX_LEN)


class ArcText(Document):
    collection = Keyword()
    file_path = Keyword()
    lang = Keyword()

    txt_len = Integer()
    file_extension = Keyword(ignore_above=KEYWORD_MAX_LEN)
    extract_text = Boolean()
    file_mime_type = Keyword(ignore_above=KEYWORD_MAX_LEN)
    file_size_kb = Integer()
    datetime_access = Date()
    datetime_modification = Date()
    datetime_meta = Date()

    data_origin = Keyword(ignore_above=KEYWORD_MAX_LEN)
    media_file = Keyword(ignore_above=KEYWORD_MAX_LEN)
    duration_seconds = Integer()
    width = Integer()
    height = Integer()

    text = Text(
        analyzer=en_ru_analyzer,
        fielddata=True,
        fielddata_frequency_filter=FIELD_DATA_FREQUENCY_FILTER
    )

    topics = Keyword(ignore_above=KEYWORD_MAX_LEN)
    topics_num = Integer()

    named_entities = Nested(NamedEntity)

    tags = Keyword(ignore_above=KEYWORD_MAX_LEN)

    data_lineage = Nested(DataLineage)
    created_at = Date()

    # TODO: tune & config
    class Index:
        name = 'arc_text'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Meta:
        dynamic = MetaField('strict')

    def get_mapping(self):
        return self._index.get_mapping()

    def save(self, **kwargs):
        return super(ArcText, self).save(**kwargs)


def create_index():
    ArcText.init()
