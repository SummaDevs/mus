# cleansing
import os

from unstructured.file_utils.filetype import STR_TO_FILETYPE

from mus.constant import constant

UNS_FILE_SIZE_MAX_KB = 1024

STATS_PRINT_CNT = 100
ERROR_MAX_CNT = 1000

skip_dir_path = {
    ".git",
}

SKIP_JSON_FILE_SET = {
    "_stats.json",  # directory statistics
}

ES_DOC_EXT = ".json"

WORKING_LANGUAGES = {
    'be',
    'bg',
    'cs',
    'ce',
    'zh',
    'de',
    'en',
    'fa',
    'fi',
    'fr',
    'ka',
    'he',
    'hi',
    'hu',
    'hy',
    'it',
    'pl',
    'ro',
    'ru',
    'sk',
    'sr',
    'uk'
}

UNSTRUCT_TEST_DOC_PATH = os.path.join(constant.BASE_DIR, "docs", "example_docs", "layout-parser-paper.pdf")
UNSTRUCT_TEST_DOC_EL_NUM = 206

EXCLUDE_MIME_TYPE_SET = {
    "inode/x-empty",
    "application/rtf",
    "text/rtf"
}
EXT_EXTRACT = dict([(k, v) for k, v in STR_TO_FILETYPE.items() if k not in EXCLUDE_MIME_TYPE_SET])
TYPE_EXTRACT_ADD_EXT_SET = {"eml"}
TYPE_EXTRACT_TEXT_SET = set(EXT_EXTRACT.keys())
TYPE_EXTRACT_EXT_SET = set((ext.name.lower() for ext in EXT_EXTRACT.values())).union(TYPE_EXTRACT_ADD_EXT_SET)

ELEMENT_TEXT_MIN_LEN = 8

el_type = {
    "element_id",
    "FigureCaption",
    "NarrativeText",
    "ListItem",
    "Title",
    "Address",
    "Table",
    "PageBreak",
    "Header",
    "Footer",
    "UncategorizedText",
    "Image",
    "Formula",
    "metadata",
    "text",
}

el_type_text = {
    "element_id",
    "NarrativeText",
    "ListItem",
    "Title",
    "Address",
    "Table",
    "UncategorizedText",
    "Formula",
    "text",
}

el_metadata = {
    "filename",
    "file_directory",
    "last_modified",
    "filetype",
    "coordinates",
    "parent_id",
    "category_depth",
    "text_as_html",
    "languages",
    "emphasized_text_contents",
    "emphasized_text_tags",
    "is_continuation",
    "detection_class_prob",
}
