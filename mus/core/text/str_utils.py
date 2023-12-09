import trafaret as t


def str_strip(
        nullable=False,
        allow_blank=False,
        min_length=None,
        max_length=None):
    main = t.String(
        allow_blank=allow_blank, min_length=min_length, max_length=max_length)

    return t.Null() | (main >> str.strip) if nullable else main >> str.strip


def utf8len(s):
    return len(s.encode('utf-8'))


def is_ascii(string):
    try:
        string.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
