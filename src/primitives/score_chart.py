from reportlab.platypus import Flowable, Frame, Spacer, Paragraph
from reportlab.graphics.shapes import Drawing, Polygon
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm

from src.enums import Colors, Spacing
from src.styles.stylesheet import CustomStyleSheet
from src.types.components import ScoreData, ScoreRangeData, ScoreNotValidData


class ScoreChartPrimitive(Flowable):

    def __init__(self, score_data: ScoreData, debug_flag: int = 0):
        self.score_data = score_data
        self.debug_flag = debug_flag

        self.enforceRangeSort()

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.score_number = _ScoreNumber(
            score_data=self.score_data,
            debug_flag=self.debug_flag,
        )
        self.score_ranges = _ScoreRanges(
            score_data=self.score_data,
            debug_flag=self.debug_flag,
        )
        self.score_description = _ScoreDescription(
            score_data=self.score_data,
            debug_flag=self.debug_flag,
        )

        self.score_number.wrapOn(self.canv, self.max_width, 1)
        self.score_ranges.wrapOn(self.canv, self.max_width, 1)
        self.score_description.wrapOn(self.canv, self.max_width, 1)

        self.height = (
            self.score_number.height
            + self.score_ranges.height
            + self.score_description.height
            + Spacing.Padding * 2
        )

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width,
            height=self.height,
            topPadding=0,
            bottomPadding=0,
            rightPadding=0,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        frame.addFromList(
            [
                self.score_number,
                Spacer(1, Spacing.Padding),
                self.score_ranges,
                Spacer(1, Spacing.Padding),
                self.score_description,
            ],
            canvas,
        )

    def enforceRangeSort(self):
        self.score_data.ranges.sort(key=lambda x: x.max_score)


container_height = 20 * mm


class _ScoreNumber(Flowable):

    def __init__(
        self, score_data: ScoreData, styles=CustomStyleSheet(), debug_flag: int = 0
    ):
        self.score_data = score_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.height = container_height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        score_color = self.score_data.current_range.color
        score_styles = {
            **self.styles.Score_Center.__dict__,
            "textColor": Colors.getTextColor(score_color).value,
        }
        score_text = str(self.score_data.score)

        if not self.score_data.is_score_valid:
            score_color = self.score_data.not_valid_data.color
            score_styles = {
                **self.styles.Title_Center.__dict__,
                "textColor": Colors.getTextColor(score_color).value,
            }
            score_text = self.score_data.not_valid_data.aux_value

        score_para = Paragraph(
            score_text,
            style=ParagraphStyle(**score_styles),
        )
        score_para.debug = self.debug_flag
        score_para.wrapOn(canvas, self.max_width, 1)

        canvas.setFillColor(score_color.value)
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

        score_para.drawOn(canvas, 0, self.height / 2 - score_para.height / 2)


class _ScoreNeedle(Drawing):

    def __init__(self, hidden: bool = False, debug_flag: int = 0):
        super().__init__()
        needle = Polygon(
            [
                3,
                0,
                6,
                5,
                0,
                5,
            ]
        )
        if not hidden:
            self.add(needle)
        self.height = 5
        self.width = 6

        self._showBoundary = debug_flag


class _ScoreRanges(Flowable):

    def __init__(
        self,
        score_data: ScoreData,
        debug_flag: int = 0,
    ):
        self.score_data = score_data
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.range_height = 1.5 * mm
        self.current_range_height = self.range_height * 2

        self.needle = _ScoreNeedle(
            hidden=not self.score_data.is_score_valid, debug_flag=self.debug_flag
        )

        self.needle.wrapOn(self.canv, self.max_width, 1)

        self.height = self.current_range_height + self.needle.height + Spacing.Padding

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        range_width = (
            self.max_width - Spacing.Padding * (len(self.score_data.ranges) - 1)
        ) / len(self.score_data.ranges)

        for i, range in enumerate(self.score_data.ranges):
            range_x = i * (range_width + Spacing.Padding)
            range_y = self.current_range_height / 4
            r_height = self.range_height

            if (
                range == self.score_data.current_range
                and self.score_data.is_score_valid
            ):
                range_y = 0
                r_height = self.current_range_height

            canvas.setFillColor(range.color.value)
            canvas.setStrokeAlpha(0)

            if self.debug_flag:
                canvas.setFillAlpha(0.5)
                canvas.setStrokeAlpha(1)

            canvas.rect(
                x=range_x,
                y=range_y,
                width=range_width,
                height=r_height,
                fill=1,
            )

        if self.debug_flag:
            canvas.setFillAlpha(0)
            canvas.setStrokeAlpha(1)
            canvas.rect(
                x=0,
                y=0,
                width=self.max_width,
                height=self.height,
            )

        current_range_index = self.score_data.ranges.index(
            self.score_data.current_range
        )
        needle_x = (
            range_width / 2
            + range_width * current_range_index
            + Spacing.Padding * current_range_index
            - self.needle.width / 2
        )
        needle_y = self.current_range_height + Spacing.Padding
        self.needle.drawOn(canvas, needle_x, needle_y)


class _ScoreDescription(Flowable):

    def __init__(
        self,
        score_data: ScoreData,
        styles=CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.score_data = score_data
        self.description = self.score_data.current_range.description
        self.min = self.score_data.min_score
        self.max = self.score_data.ranges[-1].max_score
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        description_text = self.description
        if not self.score_data.is_score_valid:
            description_text = self.score_data.not_valid_data.description
        self.description_para = Paragraph(
            description_text, style=self.styles.Caption_Bold_Center
        )
        self.min_para = Paragraph(str(self.min), style=self.styles.Caption_70)
        self.max_para = Paragraph(str(self.max), style=self.styles.Caption_70_Right)

        self.description_para.wrapOn(self.canv, self.max_width, 1)
        self.min_para.wrapOn(self.canv, self.max_width, 1)
        self.max_para.wrapOn(self.canv, self.max_width, 1)

        self.height = self.description_para.height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        self.description_para.drawOn(canvas, 0, 0)
        self.min_para.drawOn(canvas, 0, 0)
        self.max_para.drawOn(canvas, 0, 0)

        if self.debug_flag:
            canvas.setFillAlpha(0)
            canvas.setStrokeAlpha(1)
            canvas.rect(
                x=0,
                y=0,
                width=self.max_width,
                height=self.height,
            )
