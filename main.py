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
from utils.patients import input_patients

app = typer.Typer()


@app.command("generate")
def generate_report_front(
    filename: Annotated[Optional[str], typer.Argument()] = None
):
    today = datetime.now(tz=ZoneInfo("America/Lima"))

    if filename is None:
        filename = f"{int(today.timestamp())}_report.pdf"

    patients_first = input_patients(blocks=12)
    patients_second = []

    add_page = typer.confirm("\nAñadir página?")
    if add_page:
        patients_second = input_patients(blocks=13)

    y_dni = 616
    y_name = 632.5
    y_arg = 621
    y_code = 621

    extra_space = 0
    packet = io.BytesIO()
    board = canvas.Canvas(packet, pagesize=A4)

    # Draw front page
    header.draw_front(canvas=board, year=today.year, month=today.month)

    for patient in patients_first:
        body.draw_front(
            board=board,
            his=patient.his,
            age=patient.age,
            personal=patient.personal,
            ident=patient.identification,
            day=str(today.day),
            #
            y_dni=y_dni,
            y_name=y_name,
            y_arg=y_arg,
            y_code=y_code,
        )

        extra_space = len(patient.his)

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

    for p in patients_second:
        body.draw_back(
            board=board,
            his=p.his,
            age=p.age,
            personal=p.personal,
            ident=p.identification,
            day=str(today.day),
            #
            y_dni=y_dni,
            y_name=y_name,
            y_arg=y_arg,
            y_code=y_code,
        )

        extra_space = len(p.his)

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
