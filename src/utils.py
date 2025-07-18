import enum
import os


class ChoiceResponse(enum.Enum):
    YES = enum.auto()
    NO = enum.auto()
    CANCEL = enum.auto()
    OK = enum.auto()


class BaseChoice:
    def __init__(
        self, choices: dict, default_response: ChoiceResponse, *args, **kwargs
    ):
        self.choices = choices
        self.default_response = default_response

    def get_response(self, message) -> ChoiceResponse:
        choices_string = "/".join([x for x in self.choices.keys()])
        response = input(f"{message} ({choices_string})\n> ")
        return self.choices.get(response, self.default_response)


class PressAnyKey(BaseChoice):
    def __init__(
        self, choices: dict, default_response: ChoiceResponse, *args, **kwargs
    ):
        BaseChoice.__init__(self, choices, default_response, *args, **kwargs)

    def get_response(self, message) -> ChoiceResponse:
        if message:
            print(message)
        os.system("pause")
        return self.default_response


class ChoiceType(enum.Enum):
    YES_NO = enum.auto()
    PRESS_ANY_KEY = enum.auto()


_CHOICES = {
    ChoiceType.YES_NO: BaseChoice(
        {"y": ChoiceResponse.YES, "n": ChoiceResponse.NO}, ChoiceResponse.NO
    ),
    ChoiceType.PRESS_ANY_KEY: PressAnyKey({"ok": ChoiceResponse.OK}, ChoiceResponse.OK),
}


def prompt(message: str, choice_type: ChoiceType = ChoiceType.YES_NO) -> ChoiceResponse:
    return _CHOICES[choice_type].get_response(message)
