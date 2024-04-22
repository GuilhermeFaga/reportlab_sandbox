from reportlab.platypus import Flowable, Paragraph, Frame
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.units import mm

from src.primitives.icon import Icon

from src.enums import Colors, Spacing
from src.styles.stylesheet import CustomStyleSheet

from typing import Final


class IconCardData:
    def __init__(self, title: str, description: str, icon, color: str = Colors.Gray):
        self.title = title
        self.description = description
        self.icon = icon
        self.color = color


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

        self.title_para = Paragraph(self.icon_card_data.title, self.styles.Subtitle)
        self.description_para = Paragraph(
            self.icon_card_data.description, self.styles.Body
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
            leftPadding=Spacing.Padding,
            bottomPadding=Spacing.Padding,
            rightPadding=0,
            topPadding=Spacing.Padding,
            showBoundary=self.debug_flag,
        )

        icon_frame = Frame(
            x1=self.max_width - self.icon_frame_width,
            y1=0,
            width=self.icon_frame_width,
            height=self.height,
            leftPadding=0,
            bottomPadding=Spacing.Padding,
            rightPadding=Spacing.Padding,
            topPadding=Spacing.Padding,
            showBoundary=self.debug_flag,
        )

        if not self.debug_flag:
            canvas.setFillColor(self.icon_card_data.color)
            canvas.setStrokeAlpha(0)
            canvas.rect(
                x=0,
                y=0,
                width=self.max_width,
                height=self.height,
                fill=1,
            )

        text_frame.addFromList([self.title_para, self.description_para], canvas)
        icon_frame.addFromList([Icon(self.icon_card_data.icon)], canvas)
