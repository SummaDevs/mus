import traceback
from collections import defaultdict

import magic
from unstructured.partition.auto import partition
from unstructured.staging.base import convert_to_dict

from mus.constant import cons_cleansing
from mus.core.lang.detect_utils import detect_language


def is_unstructured_installed():
    try:
        elements = partition(
            cons_cleansing.UNSTRUCT_TEST_DOC_PATH, unique_element_ids=True, detect_language_per_element=True)
        el_list = convert_to_dict(elements)
        return cons_cleansing.UNSTRUCT_TEST_DOC_EL_NUM == len(el_list), el_list
    except Exception as e:
        return False, [{"error_msg": str(e)}]


def is_extract_mime_type(file_path):
    mime = magic.from_file(file_path, mime=True)

    return mime in cons_cleansing.TYPE_EXTRACT_TEXT_SET, mime


def get_elem_text(elem):
    text = ""
    try:
        if ((elem.category == "UncategorizedText" or elem.category == "text" or
             elem.category == "Table" or elem.category == "Formula") and
                len(elem.text) >= cons_cleansing.ELEMENT_TEXT_MIN_LEN):
            text = f"\n{elem.text}\n"
        elif elem.category == "Title" or elem.category == "NarrativeText" or elem.category == "Address":
            text = f"\n__{elem.category}__: {elem.text}\n"
        elif elem.category == "ListItem":
            text = f"\n{elem.text}\n"
    except AttributeError:
        traceback.print_exc()
    return text


def text_from_elements(elements, txt_dict):
    for elem in elements:

        #  it is not accurate for images:
        # meta = elem.metadata.languages

        try:
            elem_text = get_elem_text(elem)

            if elem_text:
                text_lang = detect_language(elem_text)
                lang = text_lang[0]["lang"]

                if lang in cons_cleansing.WORKING_LANGUAGES:
                    txt_dict[lang] += elem_text
        except ValueError:
            traceback.print_exc()

    return txt_dict


def extract_text(doc_path) -> (dict, str):
    txt_dict = defaultdict(str)

    try:
        elements = partition(doc_path, unique_element_ids=True, detect_language_per_element=True)

        text_from_elements(elements, txt_dict)

    except Exception as e:
        txt_meta = {"error_msg": str(e), "lang": "", "txt_len": 0}
        txt = ""
    else:
        txt = "\n\n".join((f"\n{lang:}\n{lang_text}\n" for lang, lang_text in txt_dict.items()))
        txt_meta = {"lang": list(txt_dict.keys()), "txt_len": len(txt)}

    return txt_meta, txt
