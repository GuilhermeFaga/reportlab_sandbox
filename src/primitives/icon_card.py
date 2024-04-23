from reportlab.platypus import Flowable, Paragraph, Frame
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.units import mm

from src.primitives.icon import Icon

from src.enums import Colors, Spacing
from src.styles.stylesheet import CustomStyleSheet
from src.types import IconCardData

from typing import Final


class IconCardPrimitive(Flowable):
    icon_frame_width: Final[float] = 13 * mm

    def __init__(
        self,
        icon_card_data: IconCardData,
        styles: CustomStyleSheet = CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.icon_card_data = icon_card_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        title_styles = {
            **self.styles.Subtitle.__dict__,
            "textColor": Colors.getTextColor(self.icon_card_data.color).value,
            "spaceAfter": 2,
        }
        self.title_para = Paragraph(
            self.icon_card_data.title, ParagraphStyle(**title_styles)
        )
        description_styles = {
            **self.styles.Body.__dict__,
            "textColor": Colors.getTextColor(self.icon_card_data.color).value,
            "spaceBefore": 0,
        }
        self.description_para = Paragraph(
            self.icon_card_data.description, ParagraphStyle(**description_styles)
        )

        self.title_para.debug = self.debug_flag
        self.description_para.debug = self.debug_flag

        self.title_para.wrapOn(self.canv, self.max_width - self.icon_frame_width, 0)
        self.description_para.wrapOn(
            self.canv, self.max_width - self.icon_frame_width, 0
        )

        self.height = (
            self.title_para.height
            + self.title_para.getSpaceAfter()
            + self.description_para.height
            + Spacing.Padding * 2
        )

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        text_frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width - self.icon_frame_width,
            height=self.height,
            leftPadding=Spacing.Padding * 2,
            bottomPadding=Spacing.Padding,
            rightPadding=0,
            topPadding=Spacing.Padding,
            showBoundary=self.debug_flag,
        )

        icon_size = int(8.5 * mm)
        icon = Icon(
            self.icon_card_data.icon,
            width=icon_size,
            color=self.icon_card_data.color,
            debug_flag=self.debug_flag,
        )
        icon.wrap(icon_size, icon_size)
        icon_frame = Frame(
            x1=self.max_width
            - self.icon_frame_width
            + (self.icon_frame_width - icon_size)
            - Spacing.Padding * 2,
            y1=(self.height - icon.height) / 2,
            width=icon_size,
            height=icon.height,
            leftPadding=0,
            bottomPadding=0,
            rightPadding=Spacing.Padding,
            topPadding=0,
            showBoundary=self.debug_flag,
        )

        canvas.setFillColor(self.icon_card_data.color.value)
        canvas.setStrokeAlpha(0)

        if self.debug_flag:
            canvas.setFillAlpha(0.5)
            canvas.setStrokeAlpha(1)

        canvas.rect(
            x=0,
            y=0,
            width=self.max_width,
            height=self.height,
            fill=1,
        )

        text_frame.addFromList([self.title_para, self.description_para], canvas)
        icon_frame.addFromList([icon], canvas)
