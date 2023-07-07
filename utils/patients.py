import json
from datetime import datetime
from math import ceil
from typing import Any, NamedTuple
from zoneinfo import ZoneInfo

import typer
from rich import print
from rich.prompt import Prompt


class CurrentAge(NamedTuple):
    years: int
    months: int
    days: int
    format: str


class Personal(NamedTuple):
    dni: str
    weight: str
    size: str
    hb: str


class PatientData(NamedTuple):
    personal: dict[str, str]
    identification: Any
    his: Any
    age: CurrentAge


def get_current_age(birthday: str) -> CurrentAge:
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
        format=f"{start.day}     {start.month}     {start.year}",
    )


def get_patient_data(people_data: Any, codes_data: Any) -> PatientData:
    dni = Prompt.ask("\n[blue]Número de DNI[/blue]")
    weight = Prompt.ask("[blue]Peso en kg[/blue]")
    size = Prompt.ask("[blue]Talla en cm[/blue]")
    hb = Prompt.ask("[blue]Valor de Hb[/blue]")

    age = get_current_age(birthday=people_data[dni]["birthday"])

    if age.years == 0 and age.months == 0:
        code = codes_data["RN"][f"{age.days}_days"]
    elif age.years > 5:
        code = codes_data["5_years"][f"{age.months}_months"]
    else:
        code = codes_data[f"{age.years}_years"][f"{age.months}_months"]

    return PatientData(
        personal={
            "dni": dni,
            "weight": weight,
            "size": size,
            "hb": hb,
        },
        identification=people_data[dni],
        his=code,
        age=age,
    )


def get_input_patients(blocks: int):
    with open("database/people.json", "r") as f:
        people_data = json.load(f)

    with open("database/codes.json", "r") as f:
        codes_data = json.load(f)

    patients: list[PatientData] = []

    while True:
        print(f"\n[yellow]Queda(n) {blocks} espacio(s) en la hoja.[/yellow]")

        add_patient = typer.confirm("Agregar nuevo paciente?")
        if not add_patient:
            break

        data = get_patient_data(people_data=people_data, codes_data=codes_data)

        patients.append(data)

        blocks -= ceil(len(data.his) / 3)

    return patients
