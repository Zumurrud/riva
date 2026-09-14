import logging
from functools import cache
import subprocess

from utils import (
    load_json,
    save_json,
    LANGS,
    load_wordtables,
    load_chartables,
    ensure_dir,
)
import config as cfg

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_new_names(names, wordkey):
    """
    Handles naming for 'extra' voices, those that aren't the only voice
    the character has (skins, E2s with different voices, Amiya's forms).
    """
    match wordkey.split("_")[2:]:
        case [op, outfit]:
            disc = outfit.partition("#")[0]
            name = f"{op}-{disc}"
        case [op] if op.endswith("#1"):
            disc = "e2"
            name = f"{op.partition('#')[0]}-{disc}"
        case [op] if op.startswith("amiya"):
            disc = op[5:]
            name = op
        case _:
            raise ValueError(f"extra voice with weird discriminator: {wordkey}")

    newnames = {k: (v + " " + disc.upper()) for k, v in names.items()}

    return (newnames, name)


def make_charlist():
    chartables = load_chartables()
    wordtables = load_wordtables()

    release_dates = load_json(cfg.manual("global-release.json"))
    id_to_release = {x["char_key"]: x["date_global"] for x in release_dates}

    # char_512_aprot and char_4025_aprot2 are both Shalem and have the same lines
    voices = {
        (x["charId"], x["wordKey"])
        for x in wordtables["en"]["charWords"].values()
        if x["charId"] != "char_512_aprot"
    }

    charlist = []

    for char_id, wordkey in voices:
        _, char_num, char_name = char_id.split("_")
        fulldata = chartables["en"][char_id]
        char_names = {lang: x[char_id]["name"] for lang, x in chartables.items()}

        if char_id == wordkey:
            # handle a basic voice
            newchar = {
                "fullid": char_id,
                "nameid": char_name,
                "numberid": char_num,
                "name": char_names,
            }
        else:
            # handle an extra voice, e.g. voiced skins or Amiya's extra forms
            if wordkey.endswith("_ITA") or wordkey.endswith("_CN_TOPOLECT"):
                # These don't have separate voice texts and don't need further handling
                continue

            # Only changes for Amiya, so far
            _, char_num, _ = wordkey.split("_", maxsplit=2)

            names, name_id = get_new_names(char_names, wordkey)

            newchar = {
                "fullid": wordkey,
                "nameid": name_id,
                "numberid": char_num,
                "name": names,
            }

        newchar["nation"] = fulldata["nationId"]
        newchar["rating"] = int(fulldata["rarity"][-1])
        # not tracking skin release date separately from the skin's char
        newchar["release_date"] = id_to_release[char_id]
        charlist.append(newchar)

    return sorted(charlist, key=lambda x: x["fullid"])


def make_and_save_charlist():
    charlist = make_charlist()
    logger.info(f"Loaded {len(charlist)} characters")
    # site uses it directly, but other datascript components can too
    save_json(charlist, cfg.cached("charlist.json"))
    save_json(charlist, cfg.output("charlist.json"))

    return charlist


def get_welcome():
    tables = load_wordtables()

    key = "char_002_amiya_CN_042"
    result = {}
    for lang in LANGS:
        voice_data = tables[lang]["charWords"][key]
        result[lang] = voice_data["voiceText"]

    logger.info("Texts in key found. Now saving...")
    save_json(result, cfg.output("welcome.json"))


def get_voices(wordkey, wordtables):
    # Use EN as base
    basetable = wordtables["en"]

    voices = []

    for wordid in basetable["charWords"]:
        basedata = basetable["charWords"][wordid]
        if basedata["wordKey"] != wordkey:
            continue

        voicedata = {
            "id": wordid,
            "title": {"en": basedata["voiceTitle"]},
            "text": {"en": basedata["voiceText"].replace(" ", " ")},
            "asset": basedata["voiceAsset"],
        }

        for lang in LANGS:
            if lang == "en":
                # Skip en
                continue

            try:
                langbasedata = wordtables[lang]["charWords"][wordid]
            except KeyError:
                logger.warning(f"Error getting voice in {lang} for {wordid}")
            else:
                voicedata["title"][lang] = langbasedata["voiceTitle"]
                voicedata["text"][lang] = langbasedata["voiceText"]

        voices.append(voicedata)

    return voices


# mapping lang code in the JSON to what we want the site's JS to see.
# on the site, languages will show up in the order they're listed here
LANG_MAPPING = {
    "EN": "en",
    "CN_MANDARIN": "cn",
    "CN_TOPOLECT": "cn_topolect",
    "JP": "jp",
    "KR": "kr",
    "GER": "de",
    "SPA": "es",
    "11": "es",  # FBS have been very slow to update
    "FRE": "fr",
    "ITA": "it",
    "RUS": "ru",
    "LINKAGE": "linkage",
}


@cache
def get_lang_sort_key(x):
    sort_order = {v: i for i, v in enumerate(LANG_MAPPING.values())}
    return sort_order[x]


def get_actors_from_voicedict(voicedict):
    actors = {}
    for lang, d in voicedict.items():
        try:
            actors[LANG_MAPPING[lang]] = ",".join(d["cvName"])
        except KeyError:
            logger.warning(
                f"Unknown language '{lang}' found for {d['wordkey']}, skipping"
            )

    return {k: actors[k] for k in sorted(actors.keys(), key=get_lang_sort_key)}


def get_actors(charid, wordtables):
    logger.debug(f"Checking voice actor names for {charid}")
    # JP use the native spelling of the name
    # EN use English preferred name or transliteration
    # CN use CN names even for Korean and Japanese names with kana
    # So we use JP as base
    basetable = wordtables["jp"]
    try:
        voicedict = basetable["voiceLangDict"][charid]["dict"]
    except KeyError:
        # When there are no voice data associated yet
        return {}
    native_names = get_actors_from_voicedict(voicedict)

    # Add EN names as they're often the global preferred name
    entable = wordtables["en"]
    envoicedict = entable["voiceLangDict"][charid]["dict"]
    global_names = get_actors_from_voicedict(envoicedict)

    actors = {}
    for lang in native_names:
        actors[lang] = {}
        actors[lang]["native"] = native_names[lang]
        actors[lang]["global"] = global_names[lang]

    return actors


def add_old_voices(chardata):
    manualdata = load_json(cfg.manual("old-voices.json"))

    try:
        old_voice_data = manualdata["oldvoices"][chardata["nameid"]]
    except KeyError:
        return

    logger.info(f"Adding old voice ({old_voice_data['lang']}) to {chardata['nameid']}")
    newkey = "old_" + old_voice_data["lang"]
    chardata["actors"][newkey] = old_voice_data["actor"]
    chardata["availability"].append(newkey)

    try:
        chardata["audio_path_override"][newkey] = old_voice_data["baseurl"]
    except KeyError:
        chardata["audio_path_override"] = {}
        chardata["audio_path_override"][newkey] = old_voice_data["baseurl"]

    return


def get_chardata(char):
    char_id = char["fullid"]

    wordtables = load_wordtables()
    voices = get_voices(char_id, wordtables)
    actors = get_actors(char_id, wordtables)
    availability = [k for k in actors]

    chardata = {
        "charid": char_id,
        "nameid": char["nameid"],
        "names": char["name"],
        "voices": voices,
        "actors": actors,
        "availability": availability,
    }

    add_old_voices(chardata)

    return chardata


def convert_and_write_image(sourcefile, targetfile):
    ensure_dir(targetfile)
    cwebp_params = ["-m", "6", "-alpha_q", "40", "-alpha_filter", "best"]
    run_args = ["cwebp", *cwebp_params, sourcefile, "-o", targetfile]
    subprocess.run(run_args, capture_output=True, check=True)


def process_images():
    def convert_if_needed(src, dst):
        if dst.is_file():
            logger.debug(f"{dst} already exists, skipping")
        else:
            convert_and_write_image(src, dst)

    for avapath in cfg.cached("images/avatars").glob("*.png"):
        if "#" in avapath.stem:
            _, new_stem = get_new_names({}, avapath.stem)
        else:
            new_stem = avapath.stem.split("_")[-1]

        targetpath = (
            cfg.output(*avapath.parts[1:]).with_stem(new_stem).with_suffix(".webp")
        )
        convert_if_needed(avapath, targetpath)

    for factionpath in cfg.cached("images/factions").glob("*.png"):
        targetpath = cfg.output(*factionpath.parts[1:]).with_suffix(".webp")
        convert_if_needed(factionpath, targetpath)


def get_and_write_chardata(char):
    logger.debug(f"Getting chardata for {char['fullid']}")
    chardata = get_chardata(char)
    save_json(chardata, cfg.output(f"chardata/{char['nameid']}.json"))


def process_all_characters(charlist):
    for char in charlist:
        get_and_write_chardata(char)


def get_and_save_misc_data(charlist):
    nations = {char["nation"] for char in charlist if char["nation"] is not None}

    miscdata = {"nations": sorted(nations)}

    save_json(miscdata, cfg.output("miscdata.json"))
    logger.info("Created misc data file")


def run_transformer():
    logger.info("Running")
    charlist = make_and_save_charlist()
    get_and_save_misc_data(charlist)
    process_all_characters(charlist)
    get_welcome()
