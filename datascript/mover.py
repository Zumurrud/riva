import glob
import logging
import shutil
import subprocess
from os import path

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_site_filename(orig, new_extension=None):
    root, ext = path.splitext(orig)
    if new_extension:
        ext = "." + new_extension

    match root.split("_")[2:]:
        case [op, outfit]:
            # e.g. whitw2_sale#15
            new_root = f"{op}-{outfit.partition('#')[0]}"
        case [op] if "#" in op:
            # e.g. mudrok#1, lolxh#1 - E2s with different voices
            new_root = f"{op.partition('#')[0]}-e2"
        case [op]:
            new_root = op
        case _:
            logger.error(f"Don't know how to handle operator {orig}")

    return new_root + ext


def move_chardata():
    for src_file in glob.glob("chardata/*.json"):
        dst_path = path.join(
            "..", "site", "static", "data", "chardata", get_site_filename(src_file)
        )
        shutil.copy(src_file, dst_path)

        logger.debug("Successfully copied {src_file}")

    logger.info("Successfully copied all chardata")


def convert_and_write_image(sourcefile, targetfile):
    cwebp_params = ["-m", "6", "-alpha_q", "40", "-alpha_filter", "best"]
    run_args = ["cwebp", *cwebp_params, sourcefile, "-o", targetfile]
    subprocess.run(run_args, capture_output=True, check=True)


def move_avatars():
    for avapath in glob.glob("images/avatars/*.png"):
        targetpath = path.join(
            "..",
            "site",
            "static",
            "images",
            "avatars",
            get_site_filename(avapath, new_extension="webp"),
        )

        if path.isfile(targetpath):
            logger.debug(f"{targetpath} already exists, skipping")
        else:
            convert_and_write_image(avapath, targetpath)
            logger.debug(f"Successfully moved {targetpath}")


def move_factions():
    factionpaths = glob.glob("images/factions/*.png")
    for factionpath in factionpaths:
        targetname = path.basename(factionpath).split("_")[-1]
        targetname = path.splitext(targetname)[0] + ".webp"
        targetpath = path.join("..", "site", "static", "images", "factions", targetname)
        convert_and_write_image(factionpath, targetpath)

        logger.debug("Successfully moved {targetname}")


if __name__ == "__main__":
    move_chardata()
    move_avatars()
