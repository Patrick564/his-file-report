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
from typing_extensions import Annotated

from canvas import body, header
from utils.patients import get_input_patients

app = typer.Typer()


@app.command("generate")
def generate_report(
    filename: Annotated[Optional[str], typer.Argument()] = None
):
    today = datetime.now(tz=ZoneInfo("America/Lima"))

    if filename is None:
        filename = f"{int(today.timestamp())}_report.pdf"

    patients_first = get_input_patients(blocks=12)
    patients_second = []

    add_page = typer.confirm("\nAñadir página?")
    if add_page:
        patients_second = get_input_patients(blocks=13)

    report = body.Report()

    report.draw_header_first_page(year=today.year, month=today.month)
    report.draw_body_front(patients=patients_first, today=today)

    report.add_page()

    report.draw_header_second_page(year=today.year, month=today.month)
    report.draw_body_back(patients=patients_second, today=today)

    new_pdf = PdfReader(report.save_report())
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
