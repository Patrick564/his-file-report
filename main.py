import io
import json
from datetime import datetime
from math import ceil
from typing import Optional
from zoneinfo import ZoneInfo

import typer
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from generator import his
from utils.constants import GENDER, INSURANCE, TYPE_OF_BIRTH
from utils.patients import get_current_age, get_input_patients

console = Console()
app = typer.Typer()


@app.command("generate")
def generate_report(
    filename: Annotated[Optional[str], typer.Argument()] = None
):
    """
    Genera un PDF de dos páginas con los pacientes y sus datos ingresados.
    """

    today = datetime.now(tz=ZoneInfo("America/Lima"))

    if filename is None:
        filename = f"{int(today.timestamp())}_report.pdf"

    patients_first = get_input_patients(blocks=12)
    patients_second = []

    add_page = typer.confirm("\nAñadir página?")
    if add_page:
        patients_second = get_input_patients(blocks=13)

    report = his.Report()

    report.draw_header_first_page(year=today.year, month=today.month)
    report.draw_body_front(patients=patients_first, today=today)

    report.add_page()

    report.draw_header_second_page(year=today.year, month=today.month)
    report.draw_body_back(patients=patients_second, today=today)

    new_pdf = PdfReader(report.save_report())
    exist = PdfReader(open("assets/HIS_format.pdf", "rb"))
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


# Diagnosis
@app.command("search")
def search_by_dni(
    dni: str,
    diagnosis: Annotated[bool, typer.Option("--diagnosis", "-d")] = False,
):
    """
    Busca todos los datos del paciente por DNI.
    """

    with open("database/people.json", "r") as f:
        data = json.load(f)

    person = data[dni]
    age = get_current_age(birthday=person["birthday"])

    print(f"\n[blue]Distrito:[/blue] [green]{person['district']}[/green]")
    print(f"[blue]Sector:[/blue] [green]{person['sector']}[/green]")
    print(
        f"[blue]Apellidos y nombres:[/blue] [green]{person['father_last_name']} {person['mother_last_name']}, {person['names']}[/green]"
    )
    print(
        f"[blue]Fecha de nacimiento:[/blue] [green]{age.second_format}.[/green]"
    )
    print(
        f"[blue]Edad exacta:[/blue] [green]{age.years} año(s), {age.months} mes(es) y {age.days} día(s)[/green]"
    )
    print(
        f"[blue]Tipo de seguro:[/blue] [green]{INSURANCE[person['insurance']]}[/green]"
    )
    print(f"[blue]Género:[/blue] [green]{GENDER[person['gender']]}[/green]")
    print(
        f"[blue]Tipo de parto:[/blue] [green]{TYPE_OF_BIRTH[person['type_of_birth']]}[/green]\n"
    )

    if diagnosis:
        with open("database/codes.json", "r") as f:
            codes_data = json.load(f)

        age = get_current_age(birthday=data[dni]["birthday"])

        if age.years == 0 and age.months == 0:
            code = codes_data["RN"][f"{age.days}_days"]
        elif age.years > 5:
            code = codes_data["5_years"][f"{age.months}_months"]
        else:
            code = codes_data[f"{age.years}_years"][f"{age.months}_months"]

        table = Table()

        table.add_column("CIE 10")
        table.add_column("DESCRIPCIÓN")
        table.add_column("DX")
        table.add_column("LAB 1")
        table.add_column("LAB 2")
        table.add_column("LAB 3")

        for d in code:
            table.add_row(d[0], d[1], d[2], d[3][0], d[3][1], d[3][2])

        console.print(table, "\n")


if __name__ == "__main__":
    app()
