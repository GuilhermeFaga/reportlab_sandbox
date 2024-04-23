from reportlab.platypus import Flowable, Frame, Spacer
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.units import mm

from src.primitives.title import TitlePrimitive
from src.primitives.score_chart import ScoreChartPrimitive, ScoreData, ScoreRangeData

from src.enums import Spacing


class Score(Flowable):

    def __init__(self, title: str, score_data: ScoreData, debug_flag: int = 0):
        self.title = title
        self.score_data = score_data
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.title_primitive = TitlePrimitive(self.title, debug_flag=self.debug_flag)
        self.score_group = ScoreGroup(self.score_data, debug_flag=self.debug_flag)

        self.title_primitive.wrapOn(self.canv, self.max_width, 1)
        self.score_group.wrapOn(self.canv, self.max_width, 1)

        self.height = (
            self.title_primitive.height
            + self.score_group.height
            + Spacing.Gap * 2
            + Spacing.Padding
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
                self.title_primitive,
                Spacer(1, Spacing.Gap + Spacing.Padding),
                self.score_group,
                Spacer(1, Spacing.Gap),
            ],
            canvas,
        )


class ScoreGroup(Flowable):

    def __init__(self, score_data: ScoreData, debug_flag: int = 0):
        self.score_data = score_data
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.score_chart_primitive = ScoreChartPrimitive(
            score_data=self.score_data, debug_flag=self.debug_flag
        )

        self.score_chart_primitive.wrapOn(self.canv, self.max_width, 1)

        self.height = self.score_chart_primitive.height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        right_frame_width = 42 * mm

        right_frame = Frame(
            x1=0,
            y1=0,
            width=right_frame_width,
            height=self.height,
            topPadding=0,
            bottomPadding=0,
            rightPadding=0,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        left_frame = Frame(
            x1=right_frame_width,
            y1=0,
            width=self.max_width - right_frame_width,
            height=self.height,
            topPadding=0,
            bottomPadding=0,
            rightPadding=0,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        right_frame.addFromList([self.score_chart_primitive], canvas)
        left_frame.addFromList([], canvas)