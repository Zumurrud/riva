import grabfiles
import transformer
from utils import load_json

if __name__ == "__main__":
    transformer.run_transformer()
    grabfiles.grab_avatars()
    transformer.process_images()
