from reportlab.platypus import Flowable, Paragraph, Frame
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm

from src.primitives.icon import Icon

from src.enums import Colors, Spacing
from src.styles.stylesheet import CustomStyleSheet
from src.types import GaugeCardData

from typing import Final


class GaugeCardPrimitive(Flowable):

    def __init__(
        self, card_data: GaugeCardData, styles=CustomStyleSheet(), debug_flag: int = 0
    ):
        self.card_data = card_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.left_height: float = 0
        self.right_height: float = 0

        self.left_story: list[Flowable] = []
        self.right_story: list[Flowable] = []

        title_styles = {
            **self.styles.Subtitle.__dict__,
            "spaceAfter": 2,
        }
        self.title_para = Paragraph(
            text=self.card_data.title,
            style=ParagraphStyle(**title_styles),
        )
        description_styles = {
            **self.styles.Caption_70.__dict__,
            "spaceBefore": 0,
        }
        self.description_para = Paragraph(
            text=self.card_data.description,
            style=ParagraphStyle(**description_styles),
        )
        self.value_para = Paragraph(
            text=self.card_data.level_text,
            style=self.styles.Caption_Right,
        )

        self.title_para.wrapOn(self.canv, self.max_width, 1)
        self.description_para.wrapOn(self.canv, self.max_width, 1)
        self.value_para.wrapOn(self.canv, self.max_width, 1)

        self.left_story.append(self.title_para)
        self.left_story.append(self.description_para)

        self.right_story.append(self.value_para)

        self.right_width = self.value_para._width_max + Spacing.Padding + Spacing.Gap
        self.left_width = self.max_width - self.right_width

        self.left_height += (
            self.title_para.height
            + self.title_para.getSpaceAfter()
            + self.description_para.height
            + Spacing.Padding * 2
        )

        self.right_height += (
            self.value_para.height
            + self.value_para.getSpaceAfter()
            + Spacing.Padding * 2
        )

        self.height = max(self.left_height, self.right_height)

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        left_frame = Frame(
            x1=0,
            y1=0,
            width=self.left_width,
            height=self.height,
            topPadding=Spacing.Padding,
            bottomPadding=Spacing.Padding,
            rightPadding=0,
            leftPadding=Spacing.Padding,
            showBoundary=self.debug_flag,
        )

        right_frame = Frame(
            x1=self.left_width,
            y1=0,
            width=self.right_width,
            height=self.height,
            topPadding=Spacing.Padding,
            bottomPadding=Spacing.Padding,
            rightPadding=Spacing.Gap,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        self.title_para.debug = self.debug_flag
        self.description_para.debug = self.debug_flag
        self.value_para.debug = self.debug_flag

        canvas.setFillColor(self.card_data.color.value)
        canvas.setStrokeAlpha(0)

        if self.debug_flag:
            canvas.setFillAlpha(0.5)
            canvas.setStrokeAlpha(1)

        canvas.rect(
            x=self.max_width - Spacing.Gap / 2,
            y=0,
            width=Spacing.Gap / 2,
            height=self.height,
            fill=1,
        )

        left_frame.addFromList(self.left_story, canvas)
        right_frame.addFromList(self.right_story, canvas)


icon_size: Final[int] = int(3.7 * mm)


class _Gauge(Flowable):
    def __init__(self, level: int, debug_flag: int = 0):
        self.level = level
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.height = icon_size

        return (self.max_width, self.height)

    def draw(self):
        pass
