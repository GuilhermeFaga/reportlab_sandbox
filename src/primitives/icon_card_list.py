from reportlab.platypus import Flowable, Frame, Spacer
from reportlab.pdfgen.canvas import Canvas

from src.primitives.icon_card import IconCardPrimitive, IconCardData

from src.enums import Spacing

from math import ceil


class IconCardListPrimitive(Flowable):

    def __init__(self, items: list[IconCardData], debug_flag: int = 0):
        self.items = items
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.left_height: float = 0
        self.middle_height: float = 0
        self.right_height: float = 0

        self.left_story: list[Flowable] = []
        self.middle_story: list[Flowable] = []
        self.right_story: list[Flowable] = []

        index = 0
        for item in self.items:
            icon_card = IconCardPrimitive(item, debug_flag=self.debug_flag)
            icon_card.wrapOn(self.canv, self.max_width / 3, 1)

            if index % 3 == 0:
                self.left_story.append(Spacer(1, Spacing.Padding))
                self.left_story.append(icon_card)
                self.left_story.append(Spacer(1, Spacing.Padding))
                self.left_height += icon_card.height + Spacing.Padding * 2
            elif index % 3 == 1:
                self.middle_story.append(Spacer(1, Spacing.Padding))
                self.middle_story.append(icon_card)
                self.middle_story.append(Spacer(1, Spacing.Padding))
                self.middle_height += icon_card.height + Spacing.Padding * 2
            else:
                self.right_story.append(Spacer(1, Spacing.Padding))
                self.right_story.append(icon_card)
                self.right_story.append(Spacer(1, Spacing.Padding))
                self.right_height += icon_card.height + Spacing.Padding * 2

            index += 1

        self.max_frame_height = max(
            self.left_height, self.middle_height, self.right_height
        )

        self.height = self.max_frame_height

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        self.left_frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width / 3,
            height=self.max_frame_height,
            leftPadding=Spacing.Padding,
            bottomPadding=0,
            rightPadding=Spacing.Padding,
            topPadding=0,
            showBoundary=self.debug_flag,
        )

        self.middle_frame = Frame(
            x1=self.max_width / 3,
            y1=0,
            width=self.max_width / 3,
            height=self.max_frame_height,
            leftPadding=Spacing.Padding,
            bottomPadding=0,
            rightPadding=Spacing.Padding,
            topPadding=0,
            showBoundary=self.debug_flag,
        )

        self.right_frame = Frame(
            x1=(self.max_width / 3) * 2,
            y1=0,
            width=self.max_width / 3,
            height=self.max_frame_height,
            leftPadding=Spacing.Padding,
            bottomPadding=0,
            rightPadding=Spacing.Padding,
            topPadding=0,
            showBoundary=self.debug_flag,
        )

        self.left_frame.addFromList(self.left_story, canvas)
        self.middle_frame.addFromList(self.middle_story, canvas)
        self.right_frame.addFromList(self.right_story, canvas)
