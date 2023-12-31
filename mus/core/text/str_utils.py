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


def cut_str_to_bytes(s, max_bytes):
    b = s[:max_bytes].encode('utf-8')[:max_bytes]

    if b[-1] & 0b10000000:
        last_11x_index = [i for i in range(-1, -5, -1) if b[i] & 0b11000000 == 0b11000000][0]

        # last_11x_index is negative
        last_11x = b[last_11x_index]
        last_char_length = 1
        if not last_11x & 0b00100000:
            last_char_length = 2
        elif not last_11x & 0b0010000:
            last_char_length = 3
        elif not last_11x & 0b0001000:
            last_char_length = 4

        if last_char_length > -last_11x_index:
            # remove the incomplete character
            b = b[:last_11x_index]

    return b.decode('utf-8')
