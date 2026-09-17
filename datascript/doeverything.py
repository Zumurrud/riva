import argparse
import grabfiles
import transformer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update-sources",
        "-u",
        action="store_true",
        help="Update the cached input tables before doing anything else.",
    )
    args = parser.parse_args()

    if args.update_sources:
        grabfiles.grab_tables()

    transformer.run_transformer()
    grabfiles.grab_avatars()
    transformer.process_images()
