import colorama

_SIZES = {1000000000: "{:1.2f}GB", 1000000: "{0:02.2f}MB", 1000: "{:02.2f}KB", 0: "{:02d}B"}


def get_size_label(size):
    for key, value in _SIZES.items():
        if size >= key:
            try:
                return value.format(size / key)
            except ZeroDivisionError:
                return value.format(size)


def all_of_a_in_b(a: list[str], b: list[str]) -> bool:
    """
    A slightly more accurate, but slower, matching function.

    Makes sure that every item in A is also in B. This works differently than all([x in b for x in a]) due to the
    fact that the code shown before doesn't check if x is in each string, it just makes sure that it's in the list.
    """

    # Convert all strings in both lists to lower case since we only care about the keywords.
    a = list(map(str.lower, a))
    b = list(map(str.lower, b))

    total_words = len(a)
    current_matches = 0

    for key_word in a:
        for word in b:
            if key_word in word:
                # This word was found so move on to the next
                current_matches += 1
                break

    # every word was found
    if current_matches == total_words:
        return True

    return False


class MatchResult:
    __slots__ = ("gid", "label", "platform", "url")

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


def find_closest(search_term: list, plt) -> list:
    """
    Retrieve all titles that match
    """
    matches = []

    # load the database
    plt.load()

    for key, game_title in plt.items():
        is_match = all_of_a_in_b(search_term, game_title.split())
        if is_match:
            match_result = MatchResult(int(key), game_title)
            match_result.platform = plt.title
            matches.append(match_result)

    return matches
