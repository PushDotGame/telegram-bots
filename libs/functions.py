import os


def touch_dirs(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)
    return path_to_dir


def get_id_from_bot_token(token):
    return token.split(':')[0]


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
