import argparse

import colorama
import tqdm

from src import database
from src import downloader
from src import matching
from src import settings

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.set_defaults(action=None)

    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser('search')
    search_parser.add_argument('keywords', nargs='+', help='A list of keywords to search for.')
    search_parser.add_argument('--platform', '-p', default='ALL', choices=list(database.get_all()),
                               help='Specify a platform to search.')
    search_parser.set_defaults(action='search')
    download_parser = sub_parsers.add_parser('download')
    download_parser.add_argument('gid', type=int, help='ID of the ROM provided from the search command.')
    download_parser.add_argument('-d', '--directory', help='The ROMs save directory. (overrides default directory)')
    download_parser.set_defaults(action='download')
    settings_parser = sub_parsers.add_parser('settings')
    _settings = settings_parser.add_mutually_exclusive_group()
    _settings.add_argument('-o', '--open', action='store_true',
                           help='Opens the config file in the default text editor.')
    _settings.add_argument('-r', '--restore', action='store_true', help='Resets the config file.')
    settings_parser.set_defaults(action='settings')

    args = parser.parse_args()
    settings.create_template()

    if args.action == 'search':

        # A list to store all matches
        all_matches = []

        # Convert the list of keywords to a string
        search_term = " ".join(args.keywords)

        # I
        if args.platform == 'ALL':
            total_db = len(database.PLATFORM_OBJECTS)
            progress_bar = tqdm.tqdm(desc='Searching', total=total_db, colour='green')

            for plt in database.iter_platforms():
                if args.platform.upper() == plt.title.upper():
                    all_matches.extend(matching.find_closest(args.keywords, plt))
                elif args.platform == 'ALL':
                    progress_bar.update()
                    all_matches.extend(matching.find_closest(args.keywords, plt))

            progress_bar.close()

        else:
            formatted = args.platform.replace(" ", "_").upper()
            pid = database.PlatformID[formatted]
            plt = database.PLATFORM_OBJECTS[pid]
            all_matches = matching.find_closest(args.keywords, plt)

        print(
            f"\n{colorama.Fore.RESET}Showing {len(all_matches)} results for {colorama.Fore.YELLOW}{search_term}{colorama.Fore.RESET}...")

        for result in all_matches:
            result.pretty_print(args.keywords)

    elif args.action == 'download':
        override = None
        if args.directory:
            override = args.directory

        downloader.download(args.gid, override=override)

    elif args.action == 'settings':
        if args.open:
            settings.open_in_editor()
        elif args.restore:
            settings.create_template(restore=True)
