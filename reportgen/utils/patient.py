from datetime import datetime
from math import ceil
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
        format=f"{start.day}   {start.month}    {start.year}",
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
