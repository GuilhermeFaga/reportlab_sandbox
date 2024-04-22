from reportlab.platypus import Flowable, Paragraph
from reportlab.pdfgen.canvas import Canvas

from src.enums import Colors, Spacing
from src.styles.stylesheet import CustomStyleSheet


class TitlePrimitive(Flowable):

    def __init__(
        self,
        title: str,
        styles: CustomStyleSheet = CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.title = title
        self.styles = styles
        self.debug_flag = debug_flag
        self.height = 0

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.para = Paragraph(self.title, self.styles.Title)
        self.para.wrapOn(self.canv, self.max_width, 1)

        self.height = self.para.height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        self.para.debug = self.debug_flag
        self.para.drawOn(canvas, 0, 0)

        strip = TitleStrip(height=4)
        strip.wrapOn(canvas, self.max_width - self.para._width_max - Spacing.Gap, 1)
        strip.drawOn(canvas, self.para._width_max + Spacing.Gap, 0)


class TitleStrip(Flowable):

    def __init__(self, height: float):
        self.height = height

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        return (self.max_width, self.max_height)

    def draw(self):
        canvas: Canvas = self.canv
        canvas.setFillColor(Colors.Gray)
        canvas.setStrokeAlpha(0)
        canvas.rect(
            x=0,
            y=self.max_height + self.height / 3,
            width=self.max_width,
            height=self.height,
            fill=1,
        )
