import colorama

from src import database

_SIZES = {
    1000000000: "{:1.2f}GB",
    1000000: "{0:02.2f}MB",
    1000: "{:02.2f}KB",
    0: "{:02d}B",
}


def get_size_label(size):
    for key, value in _SIZES.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)
    return size


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

    def pretty_print(self, keywords=None):
        parts = []

        print(f"[{colorama.Fore.CYAN}{self.gid}{colorama.Fore.RESET}] ", end="")
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

            if in_range:
                print(colorama.Fore.YELLOW, end="")
            else:
                print(colorama.Fore.RESET, end="")
            print(char, end="")

        print(f" {colorama.Fore.LIGHTBLUE_EX}{self.platform}{colorama.Fore.RESET}")


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
