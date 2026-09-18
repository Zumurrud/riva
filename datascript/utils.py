import json
from pathlib import Path
from functools import cache

import config as cfg

LANGS = ["en", "jp", "kr", "cn"]


def ensure_dir(file: Path):
    """
    Creates the given file's parent directory/ies, if needed.
    """
    file.parent.mkdir(parents=True, exist_ok=True)


def ensure_dir_and_write(data, dst: Path):
    """
    Writes `data` to `dst` after ensuring that the
    containing directory exists.
    """
    ensure_dir(dst)

    if type(data) == str:
        dst.write_text(data, encoding="utf-8", newline="\n")
    else:
        dst.write_bytes(data)


def save_json(data, dst: Path, prettify=True):
    indent = 2 if prettify else None
    # json.dumps doesn't add a trailing newline and
    # a lot of editors are offended by files without one
    j = json.dumps(data, ensure_ascii=False, indent=indent) + "\n"
    ensure_dir_and_write(j, dst)


def load_json(source: Path):
    return json.loads(source.read_bytes())


@cache
def load_chartable(lang):
    sourcepath = cfg.cached(lang, "character_table.json")
    return load_json(sourcepath)


def load_chartables():
    return {lang: load_chartable(lang) for lang in LANGS}


@cache
def load_wordtable(lang):
    sourcepath = cfg.cached(lang, "charword_table.json")
    return load_json(sourcepath)


def load_wordtables():
    return {lang: load_wordtable(lang) for lang in LANGS}


def get_voiced_characters(wordtable=None):
    """
    Returns an iterable of (charId, wordKey) for the supplied wordtable,
    or the EN wordtable if no wordtable is supplied.
    """
    if wordtable is None:
        wordtable = load_wordtable("en")

    # char_512_aprot and char_4025_aprot2 are both Shalem and have the same lines
    return [
        (v["charId"], k)
        for k, v in wordtable["voiceLangDict"].items()
        if k != "char_512_aprot"
    ]
