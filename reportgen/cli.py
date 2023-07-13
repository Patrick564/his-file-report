from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

import typer
from pypdf import PdfReader, PdfWriter
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from reportgen.utils.custom_types import Patients

from . import __version__
from .reports.his import Report
from .utils.constants import GENDER, INSURANCE, TYPE_OF_BIRTH
from .utils.files import load_diagnostic, load_patient
from .utils.patient import get_current_age, get_input_patients

console = Console()
app = typer.Typer()


@app.command("generate")
def generate_report(
    filename: Annotated[Optional[str], typer.Argument()] = None
) -> None:
    """
    Genera un PDF de dos páginas con los pacientes y sus datos ingresados.
    """

    today = datetime.now(tz=ZoneInfo("America/Lima"))

    if filename is None:
        filename = f"cred_{int(today.timestamp())}"

    patients: Patients = {}
    patients["first_section"] = get_input_patients(blocks=12)

    add_page = typer.confirm("\nAñadir en la segunda página?")
    if add_page:
        patients["second_section"] = get_input_patients(blocks=13)

    # PDF draw
    report = Report(patients=patients, today=today.date())

    # possible methods for Report class
    # report.draw_first_page()
    # report.add_next_page()
    # report.draw_second_page()

    report.draw_header_first_page()
    report.draw_body_front()
    report.add_page()
    report.draw_header_second_page()
    report.draw_body_back()

    # Write to PDF
    fill_report = PdfReader(report.save_report())
    empty_format = PdfReader(open("assets/HIS_format.pdf", "rb"))
    output = PdfWriter()

    first_page = empty_format.pages[0]
    second_page = empty_format.pages[1]

    first_page.merge_page(fill_report.pages[0])
    second_page.merge_page(fill_report.pages[1])

    output.add_page(first_page)
    output.add_page(second_page)

    file_report = open(f"reports/{filename}.pdf", "wb")
    output.write(file_report)
    file_report.close()

    console.print(
        f"\n[green]Reporte `{filename}.pdf` creado en la carpeta `reports`.[/green]\n"
    )


@app.command("search")
def search_by_dni(
    dni: Annotated[str, typer.Argument()],
    diagnostic: Annotated[bool, typer.Option("--diagnostic", "-d")] = False,
) -> None:
    """
    Busca todos los datos del paciente por DNI.
    """

    patient = load_patient(dni=dni)
    age = get_current_age(birthday=patient.birthday)

    console.print(
        f"""
          [blue]Distrito:[/blue]            [green]{patient.district}[/green]
          [blue]Sector:[/blue]              [green]{patient.sector}[/green]
          [blue]Apellidos y nombres:[/blue] [green]{patient.father_last_name} {patient.mother_last_name}, {patient.names}[/green]
          [blue]Fecha de nacimiento:[/blue] [green]{age.second_format}.[/green]
          [blue]Edad exacta:[/blue]         [green]{age.years} año(s), {age.months} mes(es) y {age.days} día(s)[/green]
          [blue]Tipo de seguro:[/blue]      [green]{INSURANCE[patient.insurance]}[/green]
          [blue]Género:[/blue]              [green]{GENDER[patient.gender]}[/green]
          [blue]Tipo de parto:[/blue]       [green]{TYPE_OF_BIRTH[patient.type_of_birth]}[/green]
        """
    )

    if diagnostic:
        controls = load_diagnostic(age=age)

        table = Table()

        table.add_column("CIE 10")
        table.add_column("DESCRIPCIÓN")
        table.add_column("DX")
        table.add_column("LAB 1")
        table.add_column("LAB 2")
        table.add_column("LAB 3")

        for c in controls:
            table.add_row(
                c.cie, c.description, c.dx, c.lab[0], c.lab[1], c.lab[2]
            )

        console.print(table, "\n")


@app.command("version")
def version() -> None:
    console.print(f"\n[blue]v{__version__}[/blue]\n")


if __name__ == "__main__":
    app()
