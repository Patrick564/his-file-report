import io
import math
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from reportgen.utils.constants import (
    DNI_CREATOR,
    ESTABLISHMENT,
    MONTHS_ES,
    SERVICE_PRODUCER,
)
from reportgen.utils.custom_types import PatientData


class Report:
    X_TITLE: float = 51
    Y_TITLE: float = 673.3

    X_DNI: float = 71.5
    X_NAME: float = 136
    X_ARG: float = 286
    X_CODE: float = 341.5

    def __init__(self, patients: list[list[PatientData]], today: date) -> None:
        self.packet = io.BytesIO()
        self.board = canvas.Canvas(self.packet, pagesize=A4)

        self.patients = patients
        self.today = today

    def add_next_page(self) -> None:
        self.board.showPage()

    def draw_title_one(self, x: float, y: float) -> None:
        self.board.setFontSize(7)

        self.board.drawString(x, y, str(self.today.year))
        self.board.drawString(x + 32, y, MONTHS_ES[self.today.month])
        self.board.drawString(x + 114, y, ESTABLISHMENT)
        self.board.drawString(x + 276, y, SERVICE_PRODUCER)
        self.board.drawString(x + 458, y, DNI_CREATOR)

    def draw_body_one(
        self,
        x_dni: float,
        x_name: float,
        x_arg: float,
        x_code: float,
    ) -> None:
        y_dni: float = 617
        y_name: float = 632.4
        y_arg: float = 621
        y_code: float = 621

        for patient in self.patients[0]:
            self.draw_patient_one(
                patient,
                str(self.today.day),
                x_dni,
                y_dni,
                x_name,
                y_name,
                x_arg,
                y_arg,
                x_code,
                y_code,
            )

            extra_space = len(patient.his) * 1

            y_dni -= 47.8 * math.ceil(extra_space / 3)
            y_name -= 47.8 * math.ceil(extra_space / 3)
            y_arg -= 47.8 * math.ceil(extra_space / 3)
            y_code -= 47.8 * math.ceil(extra_space / 3)

    def draw_patient_one(
        self,
        patient: PatientData,
        day: str,
        x_dni: float,
        y_dni: float,
        x_name: float,
        y_name: float,
        x_arg: float,
        y_arg: float,
        x_code: float,
        y_code: float,
    ) -> None:
        # DNI
        self.board.setFontSize(10)
        self.board.drawString(x_dni, y_dni, patient.personal["dni"])

        # Day
        self.board.setFontSize(7)
        self.board.drawString(x_dni - 17, y_dni - 8, day)

        # Home district
        self.board.drawString(
            x_dni + 74, y_dni + 1, patient.identification.district
        )

        # Population center
        self.board.drawString(
            x_dni + 74, y_dni - 18, patient.identification.sector
        )

        # Full Name
        self.board.setFontSize(6)
        self.board.drawString(
            x_name,
            y_name,
            f"{patient.identification.father_last_name} {patient.identification.mother_last_name} {patient.identification.names}",
        )

        # Birthday
        self.board.drawString(
            x_name + 210,
            y_name + 0.5,
            str(patient.age.b.day),
        )
        self.board.drawString(
            x_name + 210 + 11,
            y_name + 0.5,
            str(patient.age.b.month),
        )
        self.board.drawString(
            x_name + 210 + 22,
            y_name + 0.5,
            str(patient.age.b.year),
        )

        # Age
        self.board.setFontSize(6)
        self.board.drawString(x_arg - 85, y_arg, str(patient.age.years))
        self.board.drawString(
            x_arg - 85, y_arg - 12, str(patient.age.months)
        )
        self.board.drawString(
            x_arg - 85, y_arg - 25, str(patient.age.days)
        )

        # Size, weight and HB
        self.board.drawString(x_arg, y_arg, patient.personal["weight"])
        self.board.drawString(x_arg, y_arg - 13, patient.personal["size"])
        self.board.drawString(x_arg, y_arg - 25, patient.personal["hb"])

        # Gender
        self.board.setFontSize(10)

        if patient.identification.gender == 1:
            self.board.drawString(x_arg - 59 + 0.5, y_arg - 4, "✖")
        elif patient.identification.gender == 2:
            self.board.drawString(x_arg - 59 + 0.5, y_arg - 23, "✖")

        # Service
        self.board.drawString(x_arg + 22.5 + 0.5, y_arg - 14, "✖")
        self.board.drawString(x_arg + 36.5 + 0.5, y_arg - 14, "✖")

        # Code write
        for idx, d in enumerate(patient.his):
            self.board.setFontSize(6)

            self.board.drawString(x_code + 193 + 7, y_code, d[0])
            self.board.drawString(x_code, y_code, d[1])
            self.board.drawString(
                x_code + 170 + 3, y_code, f"{d[3][0]} {d[3][1]} {d[3][2]}"
            )

            self.board.setFontSize(10)

            if d[2] == "P":
                self.board.drawString(x_code + 137.5 + 3, y_code - 1, "✖")
            elif d[2] == "D":
                self.board.drawString(x_code + 148.5 + 3, y_code - 1, "✖")
            else:
                self.board.drawString(x_code + 159.5 + 3, y_code - 1, "✖")

            if (idx + 1) % 3 == 0 and idx != 1 and idx != 0:
                y_code -= 22.6
            else:
                y_code -= 12.6

    def draw_title_two(self, x: float, y: float) -> None:
        self.board.setFontSize(7)

        self.board.drawString(x, y, str(self.today.year))
        self.board.drawString(x + 36, y, MONTHS_ES[self.today.month])
        self.board.drawString(x + 120, y, ESTABLISHMENT)
        self.board.drawString(x + 284, y, SERVICE_PRODUCER)
        self.board.drawString(x + 473, y, DNI_CREATOR)

    def draw_body_two(self) -> None:
        y_dni: float = 616 + 58
        y_name: float = 632.5 + 58
        y_arg: float = 621 + 57
        y_code: float = 621 + 57

        for patient in self.patients[1]:
            self.draw_item_back(
                patient=patient,
                day=str(self.today.day),
                y_dni=y_dni,
                y_name=y_name,
                y_arg=y_arg,
                y_code=y_code,
            )

            extra_space = len(patient.his)

            y_dni -= (47.8 + 2.5) * math.ceil(extra_space / 3)
            y_name -= (47.8 + 2.5) * math.ceil(extra_space / 3)
            y_arg -= (47.8 + 2.5) * math.ceil(extra_space / 3)
            y_code -= (47.8 + 2.5) * math.ceil(extra_space / 3)

    def draw_item_back(
        self,
        patient: PatientData,
        day: str,
        y_dni: float,
        y_name: float,
        y_arg: float,
        y_code: float,
    ) -> None:
        X_DNI = 65.5
        X_NAME = 132
        X_ARG = 286
        x_code = 343.5

        # DNI, Home district, Population center and Day
        self.board.setFontSize(10)

        self.board.drawString(X_DNI, y_dni, patient.personal["dni"])

        self.board.setFontSize(7)

        self.board.drawString(X_DNI - 16, y_dni - 8, day)
        self.board.drawString(
            X_DNI + 74 + 3, y_dni + 1, patient.identification.district
        )
        self.board.drawString(
            X_DNI + 74 + 3, y_dni - 18, patient.identification.sector
        )

        # Full name and Birthday
        self.board.setFontSize(6)

        self.board.drawString(
            X_NAME,
            y_name,
            f"{patient.identification.father_last_name} {patient.identification.mother_last_name} {patient.identification.names}",
        )
        self.board.drawString(
            X_NAME + 217,
            y_name + 0.5,
            str(patient.age.b.day),
        )
        self.board.drawString(
            X_NAME + 217 + 11,
            y_name + 0.5,
            str(patient.age.b.month),
        )
        self.board.drawString(
            X_NAME + 217 + 22,
            y_name + 0.5,
            str(patient.age.b.year),
        )

        # Age, Gender, Weight, Size, Hb and Service
        self.board.setFontSize(6)

        self.board.drawString(X_ARG - 84 - 1, y_arg, str(patient.age.years))
        self.board.drawString(
            X_ARG - 84 - 1, y_arg - 12, str(patient.age.months)
        )
        self.board.drawString(
            X_ARG - 84 - 1, y_arg - 25, str(patient.age.days)
        )

        self.board.drawString(X_ARG, y_arg, patient.personal["weight"])
        self.board.drawString(X_ARG, y_arg - 13, patient.personal["size"])
        self.board.drawString(X_ARG, y_arg - 25, patient.personal["hb"])

        self.board.setFontSize(10)

        if patient.identification.gender == 1:
            self.board.drawString(X_ARG - 59 - 1, y_arg - 4, "✖")
        elif patient.identification.gender == 2:
            self.board.drawString(X_ARG - 59 - 1, y_arg - 23, "✖")

        self.board.drawString(X_ARG + 22.5 + 1.5, y_arg - 14, "✖")
        self.board.drawString(X_ARG + 36.5 + 1.5, y_arg - 14, "✖")

        # Code write
        for idx, d in enumerate(patient.his):
            self.board.setFontSize(6)

            self.board.drawString(x_code + 193 + 11, y_code, d[0])
            self.board.drawString(x_code, y_code, d[1])
            self.board.drawString(
                x_code + 170 + 7, y_code, f"{d[3][0]} {d[3][1]} {d[3][2]}"
            )

            self.board.setFontSize(10)

            if d[2] == "P":
                self.board.drawString(x_code + 137.5 - 4.5, y_code - 1, "✖")
            elif d[2] == "D":
                self.board.drawString(x_code + 148.5 - 4.5, y_code - 1, "✖")
            else:
                self.board.drawString(x_code + 159.5 - 4.5, y_code - 1, "✖")

            if (idx + 1) % 3 == 0 and idx != 1 and idx != 0:
                y_code -= 22.6 + 2
            else:
                y_code -= 12.6

    def generate(self) -> None:
        self.draw_title_one(self.X_TITLE, self.Y_TITLE)
        self.draw_body_one(self.X_DNI, self.X_NAME, self.X_ARG, self.X_CODE)

        self.add_next_page()

        self.draw_title_two(self.X_TITLE - 7.5, self.Y_TITLE + 56.7)
        self.draw_body_two()

    def save(self) -> io.BytesIO:
        self.board.save()
        self.packet.seek(0)

        return self.packet
