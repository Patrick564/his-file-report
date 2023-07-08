import io
import math
from datetime import datetime
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from utils.constants import (
    DNI_CREATOR,
    ESTABLISHMENT,
    MONTHS_ES,
    SERVICE_PRODUCER,
)
from utils.patients import CurrentAge, PatientData


class Report:
    def __init__(self):
        self.y_dni = 616
        self.y_name = 632.5
        self.y_arg = 621
        self.y_code = 621

        self.packet = io.BytesIO()
        self.board = canvas.Canvas(self.packet, pagesize=A4)

    def save_report(self):
        self.board.save()
        self.packet.seek(0)

        return self.packet

    def add_page(self):
        self.board.showPage()

    def draw_header_first_page(self, year: int, month: int):
        x_title = 51
        y_title = 673.3

        self.board.setFontSize(7)

        self.board.drawString(x_title, y_title, str(year))
        self.board.drawString(x_title + 32, y_title, MONTHS_ES[month])
        self.board.drawString(x_title + 114, y_title, ESTABLISHMENT)
        self.board.drawString(x_title + 276, y_title, SERVICE_PRODUCER)
        self.board.drawString(x_title + 458, y_title, DNI_CREATOR)

    def draw_header_second_page(self, year: int, month: int):
        x_title = 43.5
        y_title = 730

        self.board.setFontSize(7)

        self.board.drawString(x_title, y_title, str(year))
        self.board.drawString(x_title + 36, y_title, MONTHS_ES[month])
        self.board.drawString(x_title + 120, y_title, ESTABLISHMENT)
        self.board.drawString(x_title + 284, y_title, SERVICE_PRODUCER)
        self.board.drawString(x_title + 473, y_title, DNI_CREATOR)

    def draw_body_front(
        self,
        patients: list[PatientData],
        today: datetime,
    ):
        y_dni: float = 617
        y_name: float = 632.4
        y_arg: float = 621
        y_code: float = 621

        for patient in patients:
            self.draw_item_front(
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

            extra_space = len(patient.his) * 1

            y_dni -= 47.8 * math.ceil(extra_space / 3)
            y_name -= 47.8 * math.ceil(extra_space / 3)
            y_arg -= 47.8 * math.ceil(extra_space / 3)
            y_code -= 47.8 * math.ceil(extra_space / 3)

    def draw_item_front(
        self,
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
        X_DNI = 75.5 - 4
        X_NAME = 140 - 4
        X_ARG = 290 - 4
        x_code = 345.5 - 4

        # DNI, Home district, Population center and Day first page
        self.board.setFontSize(10)

        self.board.drawString(X_DNI, y_dni, personal["dni"])

        self.board.setFontSize(7)

        self.board.drawString(X_DNI - 17, y_dni - 8, day)
        self.board.drawString(X_DNI + 74, y_dni + 1, ident["district"])
        self.board.drawString(X_DNI + 74, y_dni - 18, ident["sector"])

        # Full name and Birthday
        self.board.setFontSize(6)

        self.board.drawString(
            X_NAME,
            y_name,
            f"{ident['father_last_name']} {ident['mother_last_name']} {ident['names']}",
        )
        self.board.drawString(X_NAME + 210, y_name + 0.5, age.format)

        # Age, Gender, Weight, Size, Sb and Service
        self.board.setFontSize(6)

        self.board.drawString(X_ARG - 84 + 1, y_arg, str(age.years))
        self.board.drawString(X_ARG - 84 + 1, y_arg - 12, str(age.months))
        self.board.drawString(X_ARG - 84 + 1, y_arg - 25, str(age.days))

        self.board.drawString(X_ARG, y_arg, personal["weight"])
        self.board.drawString(X_ARG, y_arg - 13, personal["size"])
        self.board.drawString(X_ARG, y_arg - 25, personal["hb"])

        self.board.setFontSize(10)

        if ident["gender"] == 1:
            self.board.drawString(X_ARG - 59 + 0.5, y_arg - 4, "✖")
        elif ident["gender"] == 2:
            self.board.drawString(X_ARG - 59 + 0.5, y_arg - 23, "✖")

        self.board.drawString(X_ARG + 22.5 + 0.5, y_arg - 14, "✖")
        self.board.drawString(X_ARG + 36.5 + 0.5, y_arg - 14, "✖")

        # Code write
        for idx, d in enumerate(his):
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

    def draw_body_back(
        self,
        patients: list[PatientData],
        today: datetime,
    ):
        y_dni: float = 616 + 58
        y_name: float = 632.5 + 58
        y_arg: float = 621 + 57
        y_code: float = 621 + 57

        for p in patients:
            self.draw_item_back(
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

            y_dni -= (47.8 + 2.5) * math.ceil(extra_space / 3)
            y_name -= (47.8 + 2.5) * math.ceil(extra_space / 3)
            y_arg -= (47.8 + 2.5) * math.ceil(extra_space / 3)
            y_code -= (47.8 + 2.5) * math.ceil(extra_space / 3)

    def draw_item_back(
        self,
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
        X_DNI = 75.5 - 10
        X_NAME = 140 - 11 + 3
        X_ARG = 290 - 16 + 12
        x_code = 345.5 - 8 + 3 + 3

        # DNI, Home district, Population center and Day
        self.board.setFontSize(10)

        self.board.drawString(X_DNI, y_dni, personal["dni"])

        self.board.setFontSize(7)

        self.board.drawString(X_DNI - 16, y_dni - 8, day)
        self.board.drawString(X_DNI + 74 + 3, y_dni + 1, ident["district"])
        self.board.drawString(X_DNI + 74 + 3, y_dni - 18, ident["sector"])

        # Full name and Birthday
        self.board.setFontSize(6)

        self.board.drawString(
            X_NAME,
            y_name,
            f"{ident['father_last_name']} {ident['mother_last_name']} {ident['names']}",
        )
        self.board.drawString(X_NAME + 218, y_name + 1, age.format)

        # Age, Gender, Weight, Size, Hb and Service
        self.board.setFontSize(6)

        self.board.drawString(X_ARG - 84 - 1, y_arg, str(age.years))
        self.board.drawString(X_ARG - 84 - 1, y_arg - 12, str(age.months))
        self.board.drawString(X_ARG - 84 - 1, y_arg - 25, str(age.days))

        self.board.drawString(X_ARG, y_arg, personal["weight"])
        self.board.drawString(X_ARG, y_arg - 13, personal["size"])
        self.board.drawString(X_ARG, y_arg - 25, personal["hb"])

        self.board.setFontSize(10)

        if ident["gender"] == 1:
            self.board.drawString(X_ARG - 59 - 1, y_arg - 4, "✖")
        elif ident["gender"] == 2:
            self.board.drawString(X_ARG - 59 - 1, y_arg - 23, "✖")

        self.board.drawString(X_ARG + 22.5 + 1.5, y_arg - 14, "✖")
        self.board.drawString(X_ARG + 36.5 + 1.5, y_arg - 14, "✖")

        # Code write
        for idx, d in enumerate(his):
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
