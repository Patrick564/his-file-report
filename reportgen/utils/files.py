import json

from .custom_types import Control, CurrentAge, Diagnostic, Patient


def _create_control_from_dict(**kwargs) -> Control:
    kwargs["lab"] = tuple(kwargs["lab"])

    return Control(**kwargs)


def load_patient(dni: str) -> Patient:
    with open("database/people.json", "r") as f:
        patients = json.load(f)

    return Patient(**patients[dni])


def load_diagnostic(age: CurrentAge) -> Diagnostic:
    with open("database/codes.json", "r") as f:
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
    dict_diagnostic = [dict(zip(keys, r)) for r in raw_diagnostic]

    return [_create_control_from_dict(**c) for c in dict_diagnostic]
