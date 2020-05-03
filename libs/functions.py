import os
import hashlib


def touch_dirs(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)
    return path_to_dir


def get_id_from_bot_token(token):
    return token.split(':')[0]


def list2solid(payload: list, els_to_remove: list = None):
    result = []

    for item in payload:
        if item not in result:
            result.append(item.strip())

    for el in els_to_remove or ['', None]:
        while el in result:
            result.remove(el)

    return result


def file2list(path_to_file: str, comment: str = '#', integer: bool = False):
    if not os.path.exists(path_to_file):
        return []

    rows = list()
    for _line in open(path_to_file).readlines():
        _line = _line.strip()
        if _line and not _line.startswith(comment):
            if integer:
                rows.append(int(_line))
            else:
                rows.append(_line)

    return rows


def list2file(path_to_file: str, lines: list):
    with open(path_to_file, 'w') as fp:
        fp.write('\n'.join(lines))
    return path_to_file


def append2file(path_to_file: str, line):
    with open(path_to_file, 'a') as fp:
        fp.write('\n{}'.format(line))
    return path_to_file


def overwrite_none(a, b):
    if a is not None:
        return a

    return b


def md5(s: str):
    """
    md5

    :param str s: source value
    :return: str
    """
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def text_kv(key, value, width: int = 20):
    lines = [
        '{key}'.format(key=key),
        text_right(value, width),
    ]

    return '\n'.join(lines)


def text_right(value, width: int = 20):
    return '`{value}`'.format(value=str(value).rjust(width))


def text_title(value):
    lines = list()
    lines.append('`====================`')
    lines.append('`  {value}`'.format(value=str(value)))
    lines.append('`====================`')
    return '\n'.join(lines)


def seconds2countdown(seconds: int):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)
