import logging
from pathlib import Path

import requests

import config as cfg
from utils import load_json, ensure_dir_and_write

logging.basicConfig()
logger = logging.getLogger(__name__)

FACTION_URL_TMPL = "https://raw.githubusercontent.com/Aceship/Arknight-Images/main/factions/logo_{}.png"
AVATAR_URL_TMPL = "https://raw.githubusercontent.com/fexli/ArknightsResource/main/avatar/ASSISTANT/{}.png"
JSON_URL_TMPL = "https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/{region}/gamedata/excel/{file}.json"

# handling avatar/voice AB name disagreement
AVATAR_SPECIAL_CASES = {
    "char_311_mudrok#1": "char_311_mudrok_2",
    "char_4067_lolxh#1": "char_4067_lolxh_2",
    # why isn't this a problem for amiya2, I wonder
    "char_1037_amiya3": "char_1037_amiya3_2",
}


def download(url: str, out_path: Path):
    response = requests.get(url)
    if not response.ok:
        # you'd think the requests error would be enough,
        # but it prints the URL after redirects, which can be confusing
        logger.error(f"Couldn't download {out_path} from {url}")
        response.raise_for_status()

    ensure_dir_and_write(response.content, out_path)

    logger.debug(f"Successfully downloaded {url} to {out_path}")


def grab_avatar(char_id: str):
    out_path = cfg.cached(f"images/avatars/{char_id}.png")

    if out_path.is_file():
        logger.debug(f"image already exists at {out_path}, skipping")
    else:
        if char_id in AVATAR_SPECIAL_CASES:
            url = AVATAR_URL_TMPL.format(AVATAR_SPECIAL_CASES[char_id])
        else:
            url = AVATAR_URL_TMPL.format(char_id).replace("#", "_")
        download(url, out_path)


def grab_avatars(charlist=None):
    if charlist is None:
        charlist = load_json(cfg.cached("charlist.json"))

    for char in charlist:
        grab_avatar(char["fullid"])


def grab_factions(charlist=None):
    if charlist is None:
        charlist = load_json(cfg.cached("charlist.json"))

    factions_to_grab = {
        char["nation"] for char in charlist if char["nation"] is not None
    }

    for faction in factions_to_grab:
        url = FACTION_URL_TMPL.format(faction)
        out_path = cfg.cached(f"images/factions/{faction}.png")
        download(url, out_path)


def grab_tables():
    for reg in ("en", "cn", "jp", "kr"):
        for tbl in ("charword_table", "character_table"):
            url = JSON_URL_TMPL.format(region=reg, file=tbl)
            download(url, cfg.cached(reg, f"{tbl}.json"))
