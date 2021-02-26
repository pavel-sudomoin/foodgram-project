from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

pdfmetrics.registerFont(TTFont("FreeSans", "FreeSans.ttf"))


class PDFReport:
    FONT_DATA = ('FreeSans', 'FreeSans.ttf')
    FONT_SIZE = 14
    PAGE_SIZE = (2*cm, 29.7*cm - 2*cm)

    def __init__(self, response):
        pdfmetrics.registerFont(TTFont(*self.FONT_DATA))
        self.canvas = canvas.Canvas(response)
        self.canvas.setFont(self.FONT_DATA[0], self.FONT_SIZE)

    def draw_ingredients(self, response, text):
        textobject = self.canvas.beginText(*self.PAGE_SIZE)
        for name, data in text.items():
            textobject.textLine(f"{name} ({data['unit']}) — {data['quantity']}")
        self.canvas.drawText(textobject)
    
    def close_and_save(self):
        self.canvas.showPage()
        self.canvas.save()
