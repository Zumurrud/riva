from pathlib import Path

# Inputs that can be regenerated programmatically, through download or otherwise
# charword_table.json, charlist.json, etc.
CACHED_DIR_STR = "cached_inputs"
# Inputs that are maintained by hand
MANUAL_DIR_STR = "manual_inputs"
# Output that is ready to be copied to the site
OUTPUT_DIR_STR = "output"

CACHED_DIR = Path(CACHED_DIR_STR)
MANUAL_DIR = Path(MANUAL_DIR_STR)
OUTPUT_DIR = Path(OUTPUT_DIR_STR)


def cached(*paths):
    return CACHED_DIR.joinpath(*paths)


def manual(*paths):
    return MANUAL_DIR.joinpath(*paths)


def output(*paths):
    return OUTPUT_DIR.joinpath(*paths)
