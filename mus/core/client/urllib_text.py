import urllib.request

from boilerpy3 import extractors

EXTRACTOR = extractors.CanolaExtractor()
RECOVERY_REQ_SLEEP = 3

URL_HEADERS = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def request_url_text(url):
    request = urllib.request.Request(
        url,
        headers=URL_HEADERS
    )
    doc = EXTRACTOR.get_doc_from_url(request)
    return doc.title, doc.content


def extract_url_text(url, logger, is_retry=True):
    page_title = page_contents = None
    try:
        page_title, page_contents = request_url_text(url)
    except Exception as exp:
        if "Temporary failure" in str(exp) and is_retry:
            try:
                page_title, page_contents = request_url_text(url)
            except Exception as exp:
                logger.warning("Data extraction error, url %s, message %s", url, str(exp))

    return page_title, page_contents
