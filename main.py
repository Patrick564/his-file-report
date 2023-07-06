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

from canvas.header import draw_back, draw_front
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


def draw_body(
    board: canvas.Canvas,
    his: Any,
    age: CurrentAge,
    personal: dict[str, str],
    ident: Any,
    day: str,
    #
    y_dni: float,
    y_name: float,
    y_arg: float,
    y_code: float,
):
    X_DNI = 75.5
    # Y_DNI = 616

    X_NAME = 140
    # Y_NAME = 632.5

    X_ARG = 290
    # Y_ARG = 621

    x_code = 345.5
    # y_code = 621

    # DNI, Home district, Population center first page
    board.setFontSize(10)

    board.drawString(X_DNI, y_dni, personal["dni"])

    board.setFontSize(7)

    board.drawString(X_DNI - 16, y_dni - 8, day)
    board.drawString(X_DNI + 74, y_dni + 1, ident["district"])
    board.drawString(X_DNI + 74, y_dni - 18, ident["sector"])

    # Full name and birthday first page
    board.setFontSize(6)

    board.drawString(
        X_NAME,
        y_name,
        f"{ident['father_last_name']} {ident['mother_last_name']} {ident['names']}",
    )
    board.drawString(X_NAME + 218, y_name + 1, age.format)

    # Age, gender, weight, size, hb and service first page
    board.setFontSize(6)

    board.drawString(X_ARG - 84, y_arg, str(age.years))
    board.drawString(X_ARG - 84, y_arg - 12, str(age.months))
    board.drawString(X_ARG - 84, y_arg - 25, str(age.days))

    board.drawString(X_ARG, y_arg, personal["weight"])
    board.drawString(X_ARG, y_arg - 13, personal["size"])
    board.drawString(X_ARG, y_arg - 25, personal["hb"])

    board.setFontSize(10)

    if ident["gender"] == 1:
        board.drawString(X_ARG - 59, y_arg - 4, "✖")
    elif ident["gender"] == 2:
        board.drawString(X_ARG - 59, y_arg - 23, "✖")

    board.drawString(X_ARG + 22.5, y_arg - 14, "✖")
    board.drawString(X_ARG + 36.5, y_arg - 14, "✖")

    # Code write
    for idx, d in enumerate(his):
        board.setFontSize(6)

        board.drawString(x_code + 193, y_code, d[0])
        board.drawString(x_code, y_code, d[1])
        board.drawString(
            x_code + 170, y_code, f"{d[3][0]} {d[3][1]} {d[3][2]}"
        )

        board.setFontSize(10)

        if d[2] == "P":
            board.drawString(x_code + 137.5, y_code - 1, "✖")
        elif d[2] == "D":
            board.drawString(x_code + 148.5, y_code - 1, "✖")
        else:
            board.drawString(x_code + 159.5, y_code - 1, "✖")

        if (idx + 1) % 3 == 0 and idx != 1 and idx != 0:
            y_code -= 22.6
        else:
            y_code -= 12.6


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

    free_spaces = 12
    patients_front = []

    while True:
        print(
            f"\n[yellow]Queda(n) {free_spaces} espacio(s) en la hoja.[/yellow]"
        )

        add = typer.confirm(f"Agregar paciente?")
        if not add:
            break

        patient_data = get_patient_data(
            people_data=people_data, codes_data=codes_data
        )

        patients_front.append(patient_data)

        free_spaces -= ceil(len(patient_data["his"]) / 3)

    X_CONSTANTS = 54.5
    Y_CONSTANTS = 673

    x_dni = 75.5
    y_dni = 616

    x_name = 140
    y_name = 632.5

    x_arg = 290
    y_arg = 621

    x_const = 54.5
    y_const = 673

    x_code = 345.5
    y_code = 621

    extra_space = 0
    packet = io.BytesIO()
    board = canvas.Canvas(packet, pagesize=A4)

    # Draw front page
    draw_front(canvas=board, year=today.year, month=today.month)

    for p in patients_front:
        draw_body(
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

    draw_back(canvas=board, year=today.year, month=today.month)

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
