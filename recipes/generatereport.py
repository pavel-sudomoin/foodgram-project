from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from django.http import HttpResponse


class PDFReport:
    FONT_NAME = ("FreeSans", "FreeSans.ttf")
    FONT_SIZE = 14
    SPACE_AFTER = 14
    DEFAULT_CONTENT_TYPE = "application/pdf"
    DEFAULT_FILE_NAME = "ingredients.pdf"

    def __init__(self):
        pdfmetrics.registerFont(TTFont(*self.FONT_NAME))

        self.response = HttpResponse(content_type=self.DEFAULT_CONTENT_TYPE)
        self.response[
            "Content-Disposition"
        ] = f"attachment; filename={self.DEFAULT_FILE_NAME}"

        self.doc = SimpleDocTemplate(self.response)

        self.style = ParagraphStyle(
            "CustomNormal",
            fontName=self.FONT_NAME[0],
            fontSize=self.FONT_SIZE,
            parent=getSampleStyleSheet()["Normal"],
            spaceAfter=self.SPACE_AFTER,
        )

        self.content = []

    def draw_ingredients(self, ingredients):
        for name, data in ingredients.items():
            p = Paragraph(f"{name} ({data['unit']}) - {data['quantity']}", self.style)
            self.content.append(p)

    def close_and_save(self):
        self.doc.build(self.content)
        return self.response
