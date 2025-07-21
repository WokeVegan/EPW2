import colorama

from src import database, utils
from src import settings


def all_of_a_in_b(a: list[str], b: list[str], partial: bool) -> bool:
    a = [x.lower() for x in a]
    b = [x.lower() for x in b]

    if not partial:
        return all([x in b for x in a])

    matches = 0

    for key_word in a:
        for word in b:
            if key_word in word:
                matches += 1
                break

    return matches == len(a)


class MatchResult:
    __slots__ = ("gid", "label", "platform")

    def __init__(self, gid: int, label: str):
        self.gid = gid
        self.label = label
        self.platform = None

    def pretty_print(self, keywords=None, nocolor=False):
        parts = []

        prefix = ""
        suffix = ""
        color_enabled = settings.get_color_enabled()

        if color_enabled:
            prefix = colorama.Fore.CYAN
            suffix = colorama.Fore.RESET

        utils.log(f"[{prefix}{self.gid}{suffix}] ", end="")
        for word in keywords:
            index = self.label.lower().find(word.lower())
            parts.append((index, index + len(word)))

        for index, char in enumerate(self.label):
            in_range = False

            for part in parts:
                part_min = part[0]
                part_max = part[1]
                if part_min <= index < part_max:
                    in_range = True

            if color_enabled:
                if in_range:
                    utils.log(colorama.Fore.YELLOW, end="")
                else:
                    utils.log(colorama.Fore.RESET, end="")
            utils.log(char, end="")

        prefix = ""
        suffix = ""
        color_enabled = settings.get_color_enabled()

        if color_enabled:
            prefix = colorama.Fore.CYAN
            suffix = colorama.Fore.RESET

        utils.log(f" {prefix}{self.platform}{suffix}")


def find_closest(
    search_term: list[str], plt: database.Platform, partial: bool
) -> list[MatchResult]:
    # TODO Add fuzzy search
    matches = []
    plt.load()

    for key, game_title in plt.items():
        is_match = all_of_a_in_b(search_term, game_title.split(), partial)
        if is_match:
            match_result = MatchResult(int(key), game_title)
            match_result.platform = plt.title
            matches.append(match_result)

    return matches


def search(
    keywords: list, platform: str = "", partial: bool = False
) -> list[MatchResult]:
    if not platform:
        matches = []
        for p in database.iter_platforms():
            matches.extend(find_closest(keywords, p, partial))
        return matches

    for p in database.iter_platforms():
        if platform.upper() in (
            p.title.upper(),
            *(alias.upper() for alias in p.aliases),
        ):
            return find_closest(keywords, p, partial)

    return []
