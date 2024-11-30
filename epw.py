import argparse

from src import downloader
from src import matching
from src import settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(action=None)

    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser("search")
    search_parser.add_argument(
        "keywords", nargs="+", help="A list of keywords to search for."
    )
    search_parser.add_argument(
        "--platform",
        "-p",
        default="",
        help="Specify a platform to search.",
    )
    search_parser.add_argument(
        "--partial",
        default=False,
        action="store_true",
        help="Include partial matches. ex. 'old' will match 'golden'.",
    )
    search_parser.set_defaults(action="search")
    download_parser = sub_parsers.add_parser("download")
    download_parser.add_argument(
        "gid", nargs="+", help="ID of the ROM provided from the search command."
    )
    download_parser.add_argument(
        "-d",
        "--directory",
        help="The ROMs save directory. (overrides default directory)",
    )
    download_parser.set_defaults(action="download")
    settings_parser = sub_parsers.add_parser("settings")
    _settings = settings_parser.add_mutually_exclusive_group()
    _settings.add_argument(
        "-o",
        "--open",
        action="store_true",
        help="Opens the config file in the default text editor.",
    )
    _settings.add_argument(
        "-r", "--restore", action="store_true", help="Resets the config file."
    )
    settings_parser.set_defaults(action="settings")

    args = parser.parse_args()
    settings.create_template()

    if args.action == "search":
        matches = matching.search(args.keywords, args.platform, args.partial)
        for result in matches:
            result.pretty_print(args.keywords)

    elif args.action == "download":
        for index, gid in enumerate(args.gid):
            print(f"Starting download {index+1} of {len(args.gid)}")
            downloader.download(gid, override=args.directory)

    elif args.action == "settings":
        if args.open:
            settings.open_in_editor()
        elif args.restore:
            settings.create_template(restore=True)
