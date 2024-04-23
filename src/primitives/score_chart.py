from reportlab.platypus import Flowable, Frame, Spacer, Paragraph
from reportlab.graphics.shapes import Shape, Drawing, Polygon
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.units import mm

from src.styles.stylesheet import CustomStyleSheet
from src.enums import Colors, Spacing


class ScoreRangeData:
    def __init__(self, max_score: int, color: Colors, description: str):
        self.max_score = max_score
        self.color = color
        self.description = description


class ScoreData:
    def __init__(self, score: int, ranges: list[ScoreRangeData]):
        self.score = score
        self.ranges = ranges


class ScoreChartPrimitive(Flowable):

    def __init__(self, score_data: ScoreData, debug_flag: int = 0):
        self.score_data = score_data
        self.debug_flag = debug_flag

        self.enforceRangeSort()

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.score_number = _ScoreNumber(
            score=self.score_data.score,
            color=self.current_range.color,
            debug_flag=self.debug_flag,
        )
        self.score_ranges = _ScoreRanges(
            current_range=self.current_range,
            ranges=self.score_data.ranges,
            debug_flag=self.debug_flag,
        )
        self.score_description = _ScoreDescription(
            description=self.current_range.description,
            min=self.score_data.ranges[0].max_score,
            max=self.score_data.ranges[-1].max_score,
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

    @property
    def current_range(self) -> ScoreRangeData:
        score = self.score_data.score
        for range in self.score_data.ranges:
            if score <= range.max_score:
                return range
        return self.score_data.ranges[0]


container_height = 20 * mm


class _ScoreNumber(Flowable):

    def __init__(
        self, score: int, color: Colors, styles=CustomStyleSheet(), debug_flag: int = 0
    ):
        self.score = score
        self.color = color
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.height = container_height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        score_para = Paragraph(
            str(self.score),
            style=self.styles.Score_Center,
        )
        score_para.debug = self.debug_flag
        score_para.wrapOn(canvas, self.max_width, 1)

        canvas.setFillColor(self.color.value)
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

    def __init__(self, debug_flag: int = 0):
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
        self.add(needle)
        self.height = 5
        self.width = 6

        self._showBoundary = debug_flag


class _ScoreRanges(Flowable):

    def __init__(
        self,
        current_range: ScoreRangeData,
        ranges: list[ScoreRangeData],
        debug_flag: int = 0,
    ):
        self.current_range = current_range
        self.ranges = ranges
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.range_height = 1.5 * mm
        self.current_range_height = self.range_height * 2

        self.needle = _ScoreNeedle(debug_flag=self.debug_flag)

        self.needle.wrapOn(self.canv, self.max_width, 1)

        self.height = self.current_range_height + self.needle.height + Spacing.Padding

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        range_width = (self.max_width - Spacing.Padding * (len(self.ranges) - 1)) / len(
            self.ranges
        )

        for i, range in enumerate(self.ranges):
            range_x = i * (range_width + Spacing.Padding)
            range_y = (
                0 if range == self.current_range else self.current_range_height / 4
            )
            r_height = (
                self.current_range_height
                if range == self.current_range
                else self.range_height
            )

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

        current_range_index = self.ranges.index(self.current_range)
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
        description: str,
        min: int,
        max: int,
        styles=CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.description = description
        self.min = min
        self.max = max
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.description_para = Paragraph(
            self.description, style=self.styles.Caption_Bold_Center
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
