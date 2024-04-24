from reportlab.platypus import Flowable, Paragraph, Frame
from reportlab.pdfgen.canvas import Canvas

from src.primitives.gauge_card import GaugeCardPrimitive

from src.enums import Spacing
from src.styles.stylesheet import CustomStyleSheet
from src.types import GaugeCardGroupData


class GaugeCardGroupPrimitive(Flowable):

    def __init__(
        self,
        group_data: GaugeCardGroupData,
        styles=CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.group_data = group_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.left_height: float = 0
        self.right_height: float = 0

        self.left_story: list[Flowable] = []
        self.right_story: list[Flowable] = []

        self.group_title = Paragraph(
            text=self.group_data.title,
            style=self.styles.Subtitle,
        )

        self.group_title.wrapOn(self.canv, self.max_width, 1)

        for i, card in enumerate(self.group_data.cards):
            gauge_card = GaugeCardPrimitive(
                card_data=card,
                styles=self.styles,
                debug_flag=self.debug_flag,
            )
            if i % 2 == 0:
                gauge_card.wrapOn(self.canv, self.max_width / 2, 1)
                self.left_story.append(gauge_card)
                self.left_height += gauge_card.height
            else:
                gauge_card.wrapOn(self.canv, self.max_width / 2, 1)
                self.right_story.append(gauge_card)
                self.right_height += gauge_card.height

        self.height = (
            self.group_title.height
            + Spacing.Gap
            + max(self.left_height, self.right_height)
        )

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        left_frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width / 2,
            height=self.height - self.group_title.height - Spacing.Gap,
            topPadding=0,
            bottomPadding=0,
            rightPadding=0,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        right_frame = Frame(
            x1=self.max_width / 2,
            y1=0,
            width=self.max_width / 2,
            height=self.height - self.group_title.height - Spacing.Gap,
            topPadding=0,
            bottomPadding=0,
            rightPadding=0,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        self.group_title.debug = self.debug_flag

        self.group_title.drawOn(canvas, 0, self.height - self.group_title.height)

        left_frame.addFromList(self.left_story, canvas)
        right_frame.addFromList(self.right_story, canvas)
