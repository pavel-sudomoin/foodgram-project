from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

from django.http import HttpResponse


class PDFReport:
    FONT_NAME = ("FreeSans", "FreeSans.ttf")
    FONT_SIZE = 14
    PAGE_SIZE = (2 * cm, 29.7 * cm - 2 * cm)
    DEFAULT_CONTENT_TYPE = "application/pdf"
    DEFAULT_FILE_NAME = "ingredients.pdf"

    def __init__(self):
        pdfmetrics.registerFont(TTFont(*self.FONT_NAME))

        self.response = HttpResponse(content_type=self.DEFAULT_CONTENT_TYPE)
        self.response[
            "Content-Disposition"
        ] = f"attachment; filename={self.DEFAULT_FILE_NAME}"

        self.canvas = canvas.Canvas(self.response)
        self.canvas.setFont(self.FONT_NAME[0], self.FONT_SIZE)

    def draw_ingredients(self, text):
        textobject = self.canvas.beginText(*self.PAGE_SIZE)
        for name, data in text.items():
            textobject.textLine(f"{name} ({data['unit']}) - {data['quantity']}")
        self.canvas.drawText(textobject)

    def close_and_save(self):
        self.canvas.showPage()
        self.canvas.save()
        return self.response
