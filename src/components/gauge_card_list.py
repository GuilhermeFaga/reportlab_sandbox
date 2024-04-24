from reportlab.platypus import Flowable, Frame, Spacer

from src.primitives.title import TitlePrimitive
from src.primitives.gauge_card_list import GaugeCardListPrimitive, GaugeCardListData

from src.enums import Spacing


class GaugeCardList(Flowable):

    def __init__(self, title: str, list_data: GaugeCardListData, debug_flag: int = 0):
        self.title = title
        self.list_data = list_data
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.title_primitive = TitlePrimitive(self.title, debug_flag=self.debug_flag)
        self.list_primitive = GaugeCardListPrimitive(
            self.list_data, debug_flag=self.debug_flag
        )

        self.title_primitive.wrapOn(self.canv, self.max_width, 1)
        self.list_primitive.wrapOn(self.canv, self.max_width, 1)

        self.height = (
            self.title_primitive.height + self.list_primitive.height + Spacing.Gap
        )

        return (self.max_width, self.height)

    def draw(self):

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
                Spacer(1, Spacing.Gap),
                self.list_primitive,
            ],
            self.canv,
        )
