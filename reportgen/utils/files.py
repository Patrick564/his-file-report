import json
import tomllib
from typing import Any

import tomlkit

from reportgen.utils.custom_types import (
    Config,
    Control,
    CurrentAge,
    Diagnostic,
    Patient,
)


def load_config() -> Config:
    with open("reportgen/config/config.toml", mode="rb") as f:
        config = tomllib.load(f)

    return Config(**config["user"])


def set_config(
    dni: str | None = None,
    establishment: str | None = None,
    service_producer: str | None = None,
) -> None:
    with open("reportgen/config/config.toml", encoding="utf-8") as f:
        config = tomlkit.load(f)

    if dni is not None:
        config["user"]["dni"] = dni  # type: ignore

    if establishment is not None:
        config["user"]["establishment"] = establishment  # type: ignore

    if service_producer is not None:
        config["user"]["service_producer"] = service_producer  # type: ignore

    with open("reportgen/config/config.toml", mode="w", encoding="utf-8") as f:
        tomlkit.dump(config, f)


def _create_control_from_dict(**kwargs: Any) -> Control:
    kwargs["lab"] = tuple(kwargs["lab"])

    return Control(**kwargs)


def load_patient(dni: str) -> Patient:
    with open("database/people.json", encoding="utf-8") as f:
        patients = json.load(f)

    return Patient(**patients[dni])


def load_diagnostic(age: CurrentAge) -> Diagnostic:
    with open("database/codes.json", encoding="utf-8") as f:
        diagnostics = json.load(f)

    if age.years == 0 and age.months == 0:
        raw_diagnostic = diagnostics["RN"][f"{age.days}_days"]
    elif age.years > 5:
        raw_diagnostic = diagnostics["5_years"][f"{age.months}_months"]

    else:
        raw_diagnostic = diagnostics[f"{age.years}_years"][
            f"{age.months}_months"
        ]

    keys = ["cie", "description", "dx", "lab"]
    dict_diagnostic = [
        dict(zip(keys, r)) for r in raw_diagnostic
    ]  # noqa: B905

    return [_create_control_from_dict(**c) for c in dict_diagnostic]
