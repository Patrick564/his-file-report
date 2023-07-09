from typing import NamedTuple


class Control(NamedTuple):
    cie: str
    description: str
    dx: str
    lab: tuple[str, str, str]


Diagnostic = list[Control]
