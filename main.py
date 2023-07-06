import io
import json
from datetime import date, datetime
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

from utils.age import get_age
from utils.constants import (
    DNI_CREATOR,
    ESTABLISHMENT,
    HOME_DISTRICT,
    MAX_FIRST_PAGE,
    MONTHS_ES,
    SERVICE_PRODUCER,
)

app = typer.Typer()


def write_to_pdf(
    can: Any,
    code: Any,
    person: Any,
    dates: Any,
    today: Any,
    ob: Any,
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
    can.setFontSize(10)

    can.drawString(X_DNI, y_dni, ob["dni"])

    can.setFontSize(7)

    can.drawString(X_DNI - 16, y_dni - 8, str(today.day))
    can.drawString(X_DNI + 74, y_dni + 1, HOME_DISTRICT)
    can.drawString(X_DNI + 74, y_dni - 18, "LLAMACA")

    # Full name and birth date first page
    can.setFontSize(6)

    can.drawString(
        X_NAME,
        y_name,
        f"{person['paternal_surname']} {person['mother_surname']} {person['names']}",
    )
    can.drawString(X_NAME + 218, y_name + 1, dates[0])

    # Age, gender, weight, size, hb and service first page
    can.setFontSize(6)

    can.drawString(X_ARG - 84, y_arg, dates[1]["years"])
    can.drawString(X_ARG - 84, y_arg - 12, dates[1]["months"])
    can.drawString(X_ARG - 84, y_arg - 25, dates[1]["days"])

    can.drawString(X_ARG, y_arg, ob["weight"])
    can.drawString(X_ARG, y_arg - 13, ob["size"])
    can.drawString(X_ARG, y_arg - 25, ob["hb"])

    can.setFontSize(10)

    can.drawString(X_ARG - 59, y_arg - 4, "✖")
    can.drawString(X_ARG - 59, y_arg - 23, "✖")

    can.drawString(X_ARG + 22.5, y_arg - 14, "✖")
    can.drawString(X_ARG + 36.5, y_arg - 14, "✖")

    # Code write
    for idx, d in enumerate(code):
        can.setFontSize(6)

        can.drawString(x_code + 193, y_code, d[0])
        can.drawString(x_code, y_code, d[1])
        can.drawString(x_code + 170, y_code, f"{d[3][0]} {d[3][1]} {d[3][2]}")

        can.setFontSize(10)

        if d[2] == "P":
            can.drawString(x_code + 137.5, y_code - 1, "✖")
        elif d[2] == "D":
            can.drawString(x_code + 148.5, y_code - 1, "✖")
        else:
            can.drawString(x_code + 159.5, y_code - 1, "✖")

        if (idx + 1) % 3 == 0 and idx != 1 and idx != 0:
            y_code -= 22.6
        else:
            y_code -= 12.6


def ik(pd: Any, cd: Any):
    dni = Prompt.ask("\n[blue]Número de DNI[/blue]")
    weight = Prompt.ask("[blue]Peso en kg[/blue]")
    size = Prompt.ask("[blue]Talla en cm[/blue]")
    hb = Prompt.ask("[blue]Valor de Hb[/blue]")

    person = pd[dni]
    dates = get_age(person["birth_date"])

    if dates[1]["years"] == 0 and dates[1]["months"] == 0:
        code = cd["RN"][f"{dates[1]['days']}_days"]
    else:
        code = cd[f"{dates[1]['years']}_years"][f"{dates[1]['months']}_months"]

    return {
        "dni": dni,
        "weight": weight,
        "size": size,
        "hb": hb,
        "data": pd[dni],
        "code": code,
        "dates": dates,
    }


@app.command("generate")
def generate_new_document(
    filename: Annotated[Optional[str], typer.Argument()] = ""
):
    today = datetime.now(tz=ZoneInfo("America/Lima"))

    if filename == "":
        filename = f"{int(today.timestamp())}_report.pdf"

    fill_blocks = 12
    patients = []

    with open("database/people.json", "r") as f:
        people_data = json.load(f)

    with open("database/codes.json", "r") as f:
        codes_data = json.load(f)

    while True:
        print(f"\n[yellow]Quedan {fill_blocks} espacios en la hoja.[/yellow]")

        continue_add = typer.confirm(f"Agregar paciente?")
        if not continue_add:
            break

        patients.append(ik(people_data, codes_data))

        fill_blocks -= len(patients[-1]["code"])

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

    aditional = 0

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    # Header
    c.setFontSize(7)

    c.drawString(X_CONSTANTS, Y_CONSTANTS, str(today.year))
    c.drawString(X_CONSTANTS + 32, Y_CONSTANTS, MONTHS_ES[today.month])
    c.drawString(X_CONSTANTS + 114, Y_CONSTANTS, ESTABLISHMENT)
    c.drawString(X_CONSTANTS + 276, Y_CONSTANTS, SERVICE_PRODUCER)
    c.drawString(X_CONSTANTS + 458, Y_CONSTANTS, DNI_CREATOR)

    for p in patients:
        write_to_pdf(
            can=c,
            code=p["code"],
            person=p["data"],
            dates=p["dates"],
            today=today,
            ob=p,
            y_dni=y_dni,
            y_name=y_name,
            y_arg=y_arg,
            y_code=y_code,
        )

        aditional = len(p["code"])

        y_dni -= 47.8 * ceil(aditional / 3)
        y_name -= 47.8 * ceil(aditional / 3)
        y_arg -= 47.8 * ceil(aditional / 3)
        y_code -= 47.8 * ceil(aditional / 3)

    c.save()
    packet.seek(0)

    new_pdf = PdfReader(packet)
    exist = PdfReader(open("documents/HIS_format.pdf", "rb"))
    output = PdfWriter()

    page = exist.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    output.add_page(exist.pages[1])

    st = open(f"reports/{filename}.pdf", "wb")
    output.write(st)
    st.close()

    print(
        f"\n[green]Archivo {filename}.pdf creado en la carpeta reports.[/green]\n"
    )


@app.command("search")
def search_by_dni(dni: str):
    with open("database/people.json", "r") as f:
        data = json.load(f)

    person = data[dni]

    print(f"\nSector: [green]{person['sector']}[/green]")
    print(
        f"Apellidos y nombres: [green]{person['paternal_surname']} {person['mother_surname']}, {person['names']}[/green]"
    )
    print(
        f"Fecha de nacimiento: [green]{person['birth_date']}[/green] y edad exacta: [green]{person['age']}[/green]\n"
    )


@app.command()
def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
