import grabfiles
import mover
import transformer
from extravoices import create_and_fill_in_extra_voices
from utils import load_json

if __name__ == "__main__":
    charlist, wordtables = transformer.run_transformer()
    charlist = load_json("charlist.json")
    wordtables = transformer.load_wordtables()
    create_and_fill_in_extra_voices(charlist, wordtables)

    # grabfiles.grab_factions()
    grabfiles.grab_avatars()

    mover.move_charlist()
    mover.move_chardata()
    mover.move_avatars()
