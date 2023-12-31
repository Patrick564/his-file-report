from datetime import date
from typing import Any, NamedTuple


class Config(NamedTuple):
    dni: str
    establishment: str
    service_producer: str


class Control(NamedTuple):
    cie: str
    description: str
    dx: str
    lab: tuple[str, str, str]


Diagnostic = list[Control]


class Patient(NamedTuple):
    hlc: str
    district: str
    establishment: str
    sector: str
    insurance: int
    father_last_name: str
    mother_last_name: str
    names: str
    gender: int
    birthday: str
    appointment: str
    type_of_birth: int


class CurrentAge(NamedTuple):
    years: int
    months: int
    days: int
    b: date
    format: str
    second_format: str


# class Personal(NamedTuple):
#     dni: str
#     weight: str
#     size: str
#     hb: str


class PatientData(NamedTuple):
    personal: dict[str, str]
    identification: Any
    his: Diagnostic
    age: CurrentAge


Patients = dict[str, list[PatientData]]
