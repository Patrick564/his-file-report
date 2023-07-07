from typing import Any

from reportlab.pdfgen import canvas

from utils.age import CurrentAge


def draw_front(
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
    X_DNI = 75.5 - 4
    X_NAME = 140 - 4
    X_ARG = 290 - 4
    x_code = 345.5 - 4

    # DNI, Home district, Population center and Day first page
    board.setFontSize(10)

    board.drawString(X_DNI, y_dni, personal["dni"])

    board.setFontSize(7)

    board.drawString(X_DNI - 16, y_dni - 8, day)
    board.drawString(X_DNI + 74, y_dni + 1, ident["district"])
    board.drawString(X_DNI + 74, y_dni - 18, ident["sector"])

    # Full name and Birthday
    board.setFontSize(6)

    board.drawString(
        X_NAME,
        y_name,
        f"{ident['father_last_name']} {ident['mother_last_name']} {ident['names']}",
    )
    board.drawString(X_NAME + 218, y_name + 1, age.format)

    # Age, Gender, Weight, Size, Sb and Service
    board.setFontSize(6)

    board.drawString(X_ARG - 84 + 1, y_arg, str(age.years))
    board.drawString(X_ARG - 84 + 1, y_arg - 12, str(age.months))
    board.drawString(X_ARG - 84 + 1, y_arg - 25, str(age.days))

    board.drawString(X_ARG, y_arg, personal["weight"])
    board.drawString(X_ARG, y_arg - 13, personal["size"])
    board.drawString(X_ARG, y_arg - 25, personal["hb"])

    board.setFontSize(10)

    if ident["gender"] == 1:
        board.drawString(X_ARG - 59 + 0.5, y_arg - 4, "✖")
    elif ident["gender"] == 2:
        board.drawString(X_ARG - 59 + 0.5, y_arg - 23, "✖")

    board.drawString(X_ARG + 22.5 + 0.5, y_arg - 14, "✖")
    board.drawString(X_ARG + 36.5 + 0.5, y_arg - 14, "✖")

    # Code write
    for idx, d in enumerate(his):
        board.setFontSize(6)

        board.drawString(x_code + 193 + 7, y_code, d[0])
        board.drawString(x_code, y_code, d[1])
        board.drawString(
            x_code + 170 + 3, y_code, f"{d[3][0]} {d[3][1]} {d[3][2]}"
        )

        board.setFontSize(10)

        if d[2] == "P":
            board.drawString(x_code + 137.5 + 3, y_code - 1, "✖")
        elif d[2] == "D":
            board.drawString(x_code + 148.5 + 3, y_code - 1, "✖")
        else:
            board.drawString(x_code + 159.5 + 3, y_code - 1, "✖")

        if (idx + 1) % 3 == 0 and idx != 1 and idx != 0:
            y_code -= 22.6
        else:
            y_code -= 12.6


def draw_back(
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
    X_DNI = 75.5 - 10
    X_NAME = 140 - 11 + 3
    X_ARG = 290 - 16 + 12
    x_code = 345.5 - 8 + 3 + 3

    # DNI, Home district, Population center and Day
    board.setFontSize(10)

    board.drawString(X_DNI, y_dni, personal["dni"])

    board.setFontSize(7)

    board.drawString(X_DNI - 16, y_dni - 8, day)
    board.drawString(X_DNI + 74 + 3, y_dni + 1, ident["district"])
    board.drawString(X_DNI + 74 + 3, y_dni - 18, ident["sector"])

    # Full name and Birthday
    board.setFontSize(6)

    board.drawString(
        X_NAME,
        y_name,
        f"{ident['father_last_name']} {ident['mother_last_name']} {ident['names']}",
    )
    board.drawString(X_NAME + 218, y_name + 1, age.format)

    # Age, Gender, Weight, Size, Hb and Service
    board.setFontSize(6)

    board.drawString(X_ARG - 84 - 1, y_arg, str(age.years))
    board.drawString(X_ARG - 84 - 1, y_arg - 12, str(age.months))
    board.drawString(X_ARG - 84 - 1, y_arg - 25, str(age.days))

    board.drawString(X_ARG, y_arg, personal["weight"])
    board.drawString(X_ARG, y_arg - 13, personal["size"])
    board.drawString(X_ARG, y_arg - 25, personal["hb"])

    board.setFontSize(10)

    if ident["gender"] == 1:
        board.drawString(X_ARG - 59 - 1, y_arg - 4, "✖")
    elif ident["gender"] == 2:
        board.drawString(X_ARG - 59 - 1, y_arg - 23, "✖")

    board.drawString(X_ARG + 22.5 + 1.5, y_arg - 14, "✖")
    board.drawString(X_ARG + 36.5 + 1.5, y_arg - 14, "✖")

    # Code write
    for idx, d in enumerate(his):
        board.setFontSize(6)

        board.drawString(x_code + 193 + 11, y_code, d[0])
        board.drawString(x_code, y_code, d[1])
        board.drawString(
            x_code + 170 + 7, y_code, f"{d[3][0]} {d[3][1]} {d[3][2]}"
        )

        board.setFontSize(10)

        if d[2] == "P":
            board.drawString(x_code + 137.5 - 4.5, y_code - 1, "✖")
        elif d[2] == "D":
            board.drawString(x_code + 148.5 - 4.5, y_code - 1, "✖")
        else:
            board.drawString(x_code + 159.5 - 4.5, y_code - 1, "✖")

        if (idx + 1) % 3 == 0 and idx != 1 and idx != 0:
            y_code -= 22.6 + 2
        else:
            y_code -= 12.6
