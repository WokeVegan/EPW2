import colorama
from fuzzywuzzy import fuzz

from src import database, utils
from src import settings


class MatchResult:
    __slots__ = ("gid", "label", "platform", "ratio")

    def __init__(self, gid: int, label: str):
        self.gid = gid
        self.label = label
        self.platform = None
        self.ratio = 0

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
    search_term: list[str], plt: database.Platform, minimum_ratio: int
) -> list[MatchResult]:
    matches = []
    plt.load()

    for key, game_title in plt.items():

        ratio = fuzz.partial_ratio(
            str("".join(search_term)).lower(), game_title.lower()
        )

        if ratio >= int(minimum_ratio):
            match_result = MatchResult(int(key), game_title)
            match_result.platform = plt.title
            match_result.ratio = ratio
            matches.append(match_result)

    return matches


def search(keywords: list, ratio: int, platform: str = "") -> list[MatchResult]:
    if not platform:
        matches = []
        for p in database.iter_platforms():
            matches.extend(find_closest(keywords, p, ratio))
        return matches

    for p in database.iter_platforms():
        if platform.upper() in (
            p.title.upper(),
            *(alias.upper() for alias in p.aliases),
        ):
            return find_closest(keywords, p, ratio)

    return []
