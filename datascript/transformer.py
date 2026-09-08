import logging
from functools import cache
from os import path

from utils import load_json, save_json

logging.basicConfig()
logger = logging.getLogger(__name__)

LANGS = ["en", "jp", "kr", "cn"]
MUTE_CHARS = {
    "accast",
    "acfend",
    "acguad",
    "acmedc",
    "acnipe",
    "acpion",
    "acspec",
    "acsupo",
    "aprot",
    "ccast",
    "cdfend",
    "cguard",
    "cmedic",
    "cpione",
    "csnipe",
    "cspec",
    "csuppo",
    "pithst",
    "rcast",
    "rdfend",
    "rguard",
    "rmedic",
    "rsnipe",
    "sharp2",
}


def rarity_str_to_int(raritystr):
    # Transform rarity data from e.g. TIER_6 to 6 as an integer
    return int(raritystr.split("_")[-1])


def load_chartable(lang):
    sourcepath = path.join(lang, "character_table.json")
    return load_json(sourcepath)


def load_chartables():
    return {lang: load_chartable(lang) for lang in LANGS}


def load_wordtable(lang):
    sourcepath = path.join(lang, "charword_table.json")
    return load_json(sourcepath)


def load_wordtables():
    return {lang: load_wordtable(lang) for lang in LANGS}


def make_charlist():
    chartables = load_chartables()

    charlist = []

    # Use EN as base
    for charid in chartables["en"]:
        splitid = charid.split("_")

        if splitid[0] != "char":
            continue

        charname = splitid[-1]

        if charname in MUTE_CHARS:
            logger.debug(f"Found mute char {charname}, skipping")
            continue

        newchar = {
            "fullid": charid,
            "nameid": charname,
            "numberid": splitid[1],
            "name": {},
        }

        for lang in LANGS:
            regional_name = chartables[lang][charid]["name"]
            newchar["name"][lang] = regional_name

        # Set additional data
        fulldata = chartables["en"][charid]  # just use en as base
        newchar["nation"] = fulldata["nationId"]
        rarity = rarity_str_to_int(fulldata["rarity"])
        newchar["rating"] = rarity

        charlist.append(newchar)

        if charid == "char_002_amiya":
            amiya_alter1, amiya_alter2 = make_amiya_alters_data(newchar)
            charlist.append(amiya_alter1)
            charlist.append(amiya_alter2)

    return charlist


def make_amiya_alters_data(base_amiya):
    amiya_alter1 = base_amiya.copy()
    amiya_alter2 = base_amiya.copy()

    amiya_alter1["name"] = base_amiya["name"].copy()
    for lang in amiya_alter1["name"]:
        amiya_alter1["name"][lang] = base_amiya["name"][lang] + " 2"

    amiya_alter2["name"] = base_amiya["name"].copy()
    for lang in amiya_alter2["name"]:
        amiya_alter2["name"][lang] = base_amiya["name"][lang] + " 3"

    amiya_alter1["fullid"] = "char_1001_amiya2"
    amiya_alter2["fullid"] = "char_1037_amiya3"

    amiya_alter1["nameid"] = "amiya2"
    amiya_alter2["nameid"] = "amiya3"

    amiya_alter1["numberid"] = "1001"
    amiya_alter2["numberid"] = "1037"

    return (amiya_alter1, amiya_alter2)


def make_and_save_charlist():
    charlist = make_charlist()
    logger.info(f"Loaded {len(charlist)} characters")
    save_json(charlist, "charlist.json")


def get_welcome():
    tables = load_wordtables()

    key = "char_002_amiya_CN_042"
    result = {}
    for lang in LANGS:
        voice_data = tables[lang]["charWords"][key]
        result[lang] = voice_data["voiceText"]

    logger.info("Texts in key found. Now saving...")
    save_json(result, "welcome.json")


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
    manualdata = load_json("manual.json")

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


def get_chardata(charid, wordtables, names=None):
    voices = get_voices(charid, wordtables)
    actors = get_actors(charid, wordtables)
    availability = [k for k in actors]

    chardata = {
        "charid": charid,
        "nameid": charid.split("_")[-1],
        "names": {} if names is None else names,
        "voices": voices,
        "actors": actors,
        "availability": availability,
    }

    add_old_voices(chardata)

    return chardata


def get_and_write_chardata(charid, wordtables, names=None):
    logger.debug(f"Getting chardata for {charid}")
    chardata = get_chardata(charid, wordtables, names)
    save_json(chardata, f"chardata/{charid}.json")


def process_all_characters(charlist, wordtables):
    for char in charlist:
        get_and_write_chardata(char["fullid"], wordtables, char["name"])

    return wordtables


def get_and_save_misc_data(charlist):
    nations = {char["nation"] for char in charlist if char["nation"] is not None}

    miscdata = {"nations": sorted(nations)}

    save_json(miscdata, "miscdata.json")
    logger.info("Created misc data file")


def run_transformer():
    logger.info("Running")
    make_and_save_charlist()

    charlist = load_json("charlist.json")
    wordtables = load_wordtables()

    get_and_save_misc_data(charlist)
    process_all_characters(charlist, wordtables)

    return charlist, wordtables
