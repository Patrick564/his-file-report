from reportlab.pdfgen.canvas import Canvas

from utils.constants import (
    DNI_CREATOR,
    ESTABLISHMENT,
    MONTHS_ES,
    SERVICE_PRODUCER,
)
from utils.coordinates import X_HEADER, X_HEADER_BACK, Y_HEADER, Y_HEADER_BACK


def draw_front(canvas: Canvas, year: int, month: int):
    canvas.setFontSize(7)

    canvas.drawString(X_HEADER, Y_HEADER, str(year))
    canvas.drawString(X_HEADER + 32, Y_HEADER, MONTHS_ES[month])
    canvas.drawString(X_HEADER + 114, Y_HEADER, ESTABLISHMENT)
    canvas.drawString(X_HEADER + 276, Y_HEADER, SERVICE_PRODUCER)
    canvas.drawString(X_HEADER + 458, Y_HEADER, DNI_CREATOR)


def draw_back(canvas: Canvas, year: int, month: int):
    canvas.setFontSize(7)

    canvas.drawString(X_HEADER_BACK, Y_HEADER_BACK, str(year))
    canvas.drawString(X_HEADER_BACK + 32 + 4, Y_HEADER_BACK, MONTHS_ES[month])
    canvas.drawString(X_HEADER_BACK + 114 + 6, Y_HEADER_BACK, ESTABLISHMENT)
    canvas.drawString(X_HEADER_BACK + 276 + 8, Y_HEADER_BACK, SERVICE_PRODUCER)
    canvas.drawString(X_HEADER_BACK + 458 + 15, Y_HEADER_BACK, DNI_CREATOR)
