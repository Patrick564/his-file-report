from typing import Any, NamedTuple


class Control(NamedTuple):
    cie: str
    description: str
    dx: str
    lab: list[str]


class Diagnosis(NamedTuple):
    rn: Control
    zero: Control
    one: Any
    two: Any
    three: Any
    four: Any
    five: Any
