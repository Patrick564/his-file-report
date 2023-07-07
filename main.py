import io
import json
from datetime import datetime
from math import ceil
from typing import Any, Optional
from zoneinfo import ZoneInfo

import typer
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rich import print
from rich.prompt import Prompt
from typing_extensions import Annotated

from canvas import body, header
from utils.age import CurrentAge, full_age
from utils.constants import (
    DNI_CREATOR,
    ESTABLISHMENT,
    HOME_DISTRICT,
    MAX_FIRST_PAGE,
    MONTHS_ES,
    SERVICE_PRODUCER,
)

app = typer.Typer()


def get_patient_data(people_data: Any, codes_data: Any):
    dni = Prompt.ask("\n[blue]Número de DNI[/blue]")
    weight = Prompt.ask("[blue]Peso en kg[/blue]")
    size = Prompt.ask("[blue]Talla en cm[/blue]")
    hb = Prompt.ask("[blue]Valor de Hb[/blue]")

    age = full_age(birthday=people_data[dni]["birthday"])

    if age.years == 0 and age.months == 0:
        code = codes_data["RN"][f"{age.days}_days"]
    elif age.years > 5:
        code = codes_data["5_years"][f"{age.months}_months"]
    else:
        code = codes_data[f"{age.years}_years"][f"{age.months}_months"]

    return {
        "personal": {
            "dni": dni,
            "weight": weight,
            "size": size,
            "hb": hb,
        },
        "identification": people_data[dni],
        "his": code,
        "age": age,
    }


@app.command("generate")
def generate_report_front(
    filename: Annotated[Optional[str], typer.Argument()] = None
):
    today = datetime.now(tz=ZoneInfo("America/Lima"))

    if filename is None:
        filename = f"{int(today.timestamp())}_report.pdf"

    with open("database/people.json", "r") as f:
        people_data = json.load(f)

    with open("database/codes.json", "r") as f:
        codes_data = json.load(f)

    free_spaces_front = 12
    free_spaces_back = 13
    patients_front = []
    patients_back = []

    while True:
        print(
            f"\n[yellow]Queda(n) {free_spaces_front} espacio(s) en la hoja.[/yellow]"
        )

        add_patient = typer.confirm("Agregar paciente?")
        if not add_patient:
            break

        patient_data = get_patient_data(
            people_data=people_data, codes_data=codes_data
        )

        patients_front.append(patient_data)

        free_spaces_front -= ceil(len(patient_data["his"]) / 3)

    add_page = typer.confirm("\nAñadir página?")
    if add_page:
        while True:
            print(
                f"\n[yellow]Queda(n) {free_spaces_back} espacio(s) en la hoja.[/yellow]"
            )

            add_patient = typer.confirm("Agregar paciente?")
            if not add_patient:
                break

            patient_data = get_patient_data(
                people_data=people_data, codes_data=codes_data
            )

            patients_back.append(patient_data)

            free_spaces_back -= ceil(len(patient_data["his"]) / 3)

    y_dni = 616
    y_name = 632.5
    y_arg = 621
    y_code = 621

    extra_space = 0
    packet = io.BytesIO()
    board = canvas.Canvas(packet, pagesize=A4)

    # Draw front page
    header.draw_front(canvas=board, year=today.year, month=today.month)

    for p in patients_front:
        body.draw_front(
            board=board,
            his=p["his"],
            age=p["age"],
            personal=p["personal"],
            ident=p["identification"],
            day=str(today.day),
            #
            y_dni=y_dni,
            y_name=y_name,
            y_arg=y_arg,
            y_code=y_code,
        )

        extra_space = len(p["his"])

        y_dni -= 47.8 * ceil(extra_space / 3)
        y_name -= 47.8 * ceil(extra_space / 3)
        y_arg -= 47.8 * ceil(extra_space / 3)
        y_code -= 47.8 * ceil(extra_space / 3)

    # Draw back page
    board.showPage()

    y_dni = 616 + 58
    y_name = 632.5 + 58
    y_arg = 621 + 57
    y_code = 621 + 57

    header.draw_back(canvas=board, year=today.year, month=today.month)

    for p in patients_back:
        body.draw_back(
            board=board,
            his=p["his"],
            age=p["age"],
            personal=p["personal"],
            ident=p["identification"],
            day=str(today.day),
            #
            y_dni=y_dni,
            y_name=y_name,
            y_arg=y_arg,
            y_code=y_code,
        )

        extra_space = len(p["his"])

        y_dni -= (47.8 + 2.5) * ceil(extra_space / 3)
        y_name -= (47.8 + 2.5) * ceil(extra_space / 3)
        y_arg -= (47.8 + 2.5) * ceil(extra_space / 3)
        y_code -= (47.8 + 2.5) * ceil(extra_space / 3)

    board.save()
    packet.seek(0)

    new_pdf = PdfReader(packet)
    exist = PdfReader(open("documents/HIS_format.pdf", "rb"))
    output = PdfWriter()

    front = exist.pages[0]
    back = exist.pages[1]

    front.merge_page(new_pdf.pages[0])
    back.merge_page(new_pdf.pages[1])

    output.add_page(front)
    output.add_page(back)

    st = open(f"reports/{filename}.pdf", "wb")
    output.write(st)
    st.close()

    print(
        f"\n[green]Archivo `{filename}.pdf` creado en la carpeta `reports`.[/green]\n"
    )


@app.command("search")
def search_by_dni(dni: str):
    with open("database/people.json", "r") as f:
        data = json.load(f)

    person = data[dni]

    print(f"\nSector: [green]{person['sector']}[/green]")
    print(
        f"Apellidos y nombres: [green]{person['father_last_name']} {person['mother_last_name']}, {person['names']}[/green]"
    )
    print(
        f"Fecha de nacimiento: [green]{person['birthday']}[/green] y edad exacta: [green]12[/green]\n"
    )


if __name__ == "__main__":
    app()
