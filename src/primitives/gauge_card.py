from reportlab.platypus import Flowable, Paragraph, Frame
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm

from src.primitives.icon import Icon

from src.enums import Colors, Spacing, SvgPath
from src.styles.stylesheet import CustomStyleSheet
from src.types.components import GaugeCardData

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

        title_styles = self.styles.customStyle(
            style=self.styles.Body,
            spaceAfter=2,
        )
        self.title_para = Paragraph(
            text=self.card_data.title,
            style=title_styles,
        )
        description_styles = self.styles.customStyle(
            style=self.styles.Caption_70,
            spaceBefore=0,
        )
        self.description_para = Paragraph(
            text=self.card_data.description,
            style=description_styles,
        )
        self.value_para = Paragraph(
            text=self.card_data.level_text,
            style=self.styles.Body_Right,
        )
        self.gauge = _Gauge(level=self.card_data.level, debug_flag=self.debug_flag)

        self.title_para.wrapOn(self.canv, self.max_width, 1)
        self.description_para.wrapOn(self.canv, self.max_width, 1)
        self.value_para.wrapOn(self.canv, self.max_width - Spacing.Gap / 2, 1)
        self.gauge.wrapOn(self.canv, self.max_width - Spacing.Gap / 2, 1)

        self.left_story.append(self.title_para)
        self.left_story.append(self.description_para)

        self.right_story.append(self.gauge)
        self.right_story.append(self.value_para)

        self.right_width = (
            max(self.gauge.width, self.value_para._width_max)
            + Spacing.Padding
            + Spacing.Gap
        )
        self.left_width = self.max_width - self.right_width

        self.left_height += (
            self.title_para.height
            + self.title_para.getSpaceAfter()
            + self.description_para.height
            + Spacing.Padding * 2
        )

        self.right_height += (
            self.gauge.height
            + self.value_para.getSpaceBefore()
            + self.value_para.height
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


icon_size: Final[int] = int(3.8 * mm)
gauges_count: Final[int] = 3


class _Gauge(Flowable):
    def __init__(self, level: int, debug_flag: int = 0):
        self.level = level
        self.debug_flag = debug_flag

        if level < 0:
            self.level = 0
        if level > gauges_count:
            self.level = gauges_count

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.icon = Icon(
            SvgPath.Warning,
            height=icon_size,
            color=Colors.DarkGray,
            debug_flag=self.debug_flag,
        )
        self.active_icon = Icon(
            SvgPath.Warning,
            height=icon_size,
            color=Colors.Black_70,
            debug_flag=self.debug_flag,
        )

        self.icon.wrapOn(self.canv, self.max_width, 1)
        self.active_icon.wrapOn(self.canv, self.max_width, 1)

        self.width = self.icon.width * gauges_count + Spacing.Padding * (
            gauges_count - 1
        )
        self.height = self.icon.height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        for i in range(gauges_count):
            icon_x = (
                self.max_width - i * self.icon.width - Spacing.Gap - Spacing.Padding * i
            )
            if i < abs(self.level - gauges_count):
                self.icon.drawOn(canvas, icon_x, 0)
            else:
                self.active_icon.drawOn(canvas, icon_x, 0)
