from reportlab.platypus import Flowable, Frame, Spacer
from reportlab.pdfgen.canvas import Canvas

from src.primitives.title import TitlePrimitive
from src.primitives.icon_card_list import (
    IconCardListPrimitive,
    IconCardPrimitive,
    IconCardData,
)

from src.enums import Spacing

from math import ceil


class IconCardList(Flowable):

    def __init__(self, items: list[IconCardData], title: str, debug_flag: int = 0):
        self.items = items
        self.title = title
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.title_primitive = TitlePrimitive(self.title, debug_flag=self.debug_flag)
        self.icon_card_list_primitive = IconCardListPrimitive(
            self.items, debug_flag=self.debug_flag
        )

        self.title_primitive.wrapOn(self.canv, self.max_width, 1)
        self.icon_card_list_primitive.wrapOn(self.canv, self.max_width, 1)

        self.height = (
            self.title_primitive.height
            + self.icon_card_list_primitive.height
            + Spacing.Gap
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
                self.icon_card_list_primitive,
            ],
            self.canv,
        )
