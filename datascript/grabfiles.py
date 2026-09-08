import logging
from os import path

import requests

from utils import load_json

logging.basicConfig()
logger = logging.getLogger(__name__)

faction_base_url = "https://raw.githubusercontent.com/Aceship/Arknight-Images/main/factions/logo_{}.png"

avatar_base_url = "https://raw.githubusercontent.com/fexli/ArknightsResource/main/avatar/ASSISTANT/{}.png"
avatar_name_special_cases = {
    # handling avatar/voice AB name disagreement
    "char_311_mudrok#1": "char_311_mudrok_2",
    "char_4067_lolxh#1": "char_4067_lolxh_2",
    # why isn't this a problem for amiya2?
    "char_1037_amiya3": "char_1037_amiya3_2",
}


def download_image(url, target):
    response = requests.get(url)
    if not response.ok:
        logger.warning(f"Couldn't download {target} from {url}: got {response}")
        return

    with open(target, "wb") as targetfile:
        targetfile.write(response.content)

    logger.debug(f"Successfully downloaded image {url} to {target}")


def grab_avatar(char):
    fullid = char["fullid"]
    target = path.join("images", "avatars", f"{fullid}.png")

    if path.isfile(target):
        logger.debug(f"Image already exists at {target}. Skipping...")
    else:
        if fullid in avatar_name_special_cases:
            url = avatar_base_url.format(avatar_name_special_cases[fullid])
        else:
            url = avatar_base_url.format(fullid).replace("#", "_")
        download_image(url, target)


def grab_avatars():
    charlist = load_json("charlist.json")
    for char in charlist:
        grab_avatar(char)


def grab_factions():
    # This will require charlist.json that also contains nation data
    # Since those are the faction images we'll be taking
    charlist = load_json("charlist.json")

    factions_to_grab = []
    for char in charlist:
        nation = char["nation"]
        if nation is not None and nation not in factions_to_grab:
            factions_to_grab.append(nation)

    for faction in factions_to_grab:
        url = faction_base_url.format(faction)
        download_image(url, f"images/factions/{faction}.png")
