import json
from calendar import monthrange
from dataclasses import dataclass, field
from datetime import date, datetime
from math import ceil
from typing import Any, NamedTuple
from zoneinfo import ZoneInfo

import typer
from rich import print
from rich.prompt import Prompt

from reportgen.utils.custom_types import CurrentAge, PatientData
from reportgen.utils.files import load_diagnostic, load_patient


def current_age(birthday: str) -> CurrentAge:
    start = datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S").date()
    today = datetime.now(tz=ZoneInfo("America/Lima")).date()

    difference = today - start

    years = difference.days // 365
    months = (difference.days % 365) // 30
    days = (difference.days % 365) % 30

    return CurrentAge(
        years=abs(years),
        months=abs(months),
        days=abs(days),
        b=start,
        format=f"{start.day}     {start.month}     {start.year}",
        second_format=f"{start.day}/{start.month}/{start.year}",
    )


def input_patients(blocks: int) -> list[PatientData]:
    patients: list[PatientData] = []

    while True:
        print(f"\n[yellow]Queda(n) {blocks} espacio(s) en la hoja.[/yellow]")

        add_patient = typer.confirm("Agregar nuevo paciente?")
        if not add_patient:
            break

        dni = Prompt.ask("\n[blue]Número de DNI[/blue]")
        weight = Prompt.ask("[blue]Peso en kg[/blue]")
        size = Prompt.ask("[blue]Talla en cm[/blue]")
        hb = Prompt.ask("[blue]Valor de Hb[/blue]")

        patient = load_patient(dni=dni)
        age = current_age(birthday=patient.birthday)
        his = load_diagnostic(age=age)

        patients.append(
            PatientData(
                personal={
                    "dni": dni,
                    "weight": weight,
                    "size": size,
                    "hb": hb,
                },
                identification=patient,
                his=his,
                age=age,
            )
        )

        blocks -= ceil(len(his) / 3)

    return patients


GENDER = {0: "NO ESPECIFICADO", 1: "MASCULINO", 2: "FEMENINO"}

INSURANCE = {
    0: "NO ESPECIFICADO",
    1: "SIS",
    2: "ESSALUD",
    3: "OTRO",
}


class Age(NamedTuple):
    years: int
    months: int
    days: int

    def __str__(self) -> str:
        return (
            f"{self.years} año(s), {self.months} mes(es) y {self.days} día(s)"
        )


class Control(NamedTuple):
    cie: str
    description: str
    dx: str
    lab: tuple[str, str, str]


@dataclass
class TempPatient:
    dni: str
    hlc: str = field(init=False)
    district: str = field(init=False)
    establishment: str = field(init=False)
    sector: str = field(init=False)
    insurance: str = field(init=False)
    full_name: str = field(init=False)
    gender: str = field(init=False)
    birthday: date = field(init=False)
    age: Age = field(init=False)
    appointment: str = field(init=False)
    type_of_birth: int = field(init=False)
    diagnostic: list[Control] = field(init=False)
    age_diagnostic: Age = field(init=False)

    def __post_init__(self) -> None:
        patient = self.load_from_json()

        self.hlc = patient["hlc"]
        self.district = patient["district"]
        self.establishment = patient["establishment"]
        self.sector = patient["sector"]
        self.insurance = INSURANCE[int(patient["insurance"])]
        self.full_name = f"{patient['father_last_name']} {patient['mother_last_name']}, {patient['names']}"
        self.gender = GENDER[int(patient["gender"])]
        self.birthday = datetime.strptime(
            patient["birthday"], "%Y-%m-%d %H:%M:%S"
        ).date()
        self.age = self.current_age()
        self.appointment = patient["appointment"]
        self.type_of_birth = patient["type_of_birth"]
        self.diagnostic = self.load_diagnostic()

    def load_from_json(self) -> Any:
        with open("database/people.json", encoding="utf-8") as f:
            patients = json.load(f)

        return patients[f"{self.dni}"]

    def current_age(self) -> Age:
        year, month, day, *_ = datetime.now(
            tz=ZoneInfo("America/Lima")
        ).timetuple()

        if day < self.birthday.day:
            month -= 1
            day += monthrange(self.birthday.year, self.birthday.month)[1]

        if month < self.birthday.month:
            year -= 1
            month += 12

        return Age(
            year - self.birthday.year,
            month - self.birthday.month,
            day - self.birthday.day,
        )

    def load_diagnostic(self) -> list[Control]:
        with open("database/codes.json", encoding="utf-8") as f:
            diagnostics = json.load(f)

        # h = Age(0, 0, 0)

        try:
            if self.age.years == 0 and self.age.months == 0:
                raw_diagnostic = diagnostics["RN"][f"{self.age.days}_days"]
            elif self.age.years > 5:
                raw_diagnostic = diagnostics["5_years"][
                    f"{self.age.months}_months"
                ]
            else:
                raw_diagnostic = diagnostics[f"{self.age.years}_years"][
                    f"{self.age.months}_months"
                ]
        except KeyError:
            # for i in range(1, 8):
            # print(i)
            raw_diagnostic = []
            # print(key)

        return [
            Control(
                cie=d[0],
                description=d[1],
                dx=d[2],
                lab=tuple(d[3]),  # type: ignore
            )
            for d in raw_diagnostic
        ]
