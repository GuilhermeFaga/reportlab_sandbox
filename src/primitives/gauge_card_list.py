from reportlab.platypus import Flowable, Frame, Spacer

from src.primitives.gauge_card_group import GaugeCardGroupPrimitive

from src.enums import Spacing
from src.styles.stylesheet import CustomStyleSheet
from src.types import GaugeCardListData


class GaugeCardListPrimitive(Flowable):

    def __init__(
        self,
        list_data: GaugeCardListData,
        styles=CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.list_data = list_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.story: list[Flowable] = []

        self.height = 0

        for i, group in enumerate(self.list_data.groups):
            group_primitive = GaugeCardGroupPrimitive(
                group_data=group,
                styles=self.styles,
                debug_flag=self.debug_flag,
            )
            group_primitive.wrapOn(self.canv, self.max_width, 1)

            self.story.append(group_primitive)
            self.height += group_primitive.height

            if (i + 1) != len(self.list_data.groups):
                self.story.append(Spacer(1, Spacing.Gap))
                self.height += Spacing.Gap

        self.height += Spacing.Padding * 2

        return (self.max_width, self.height)

    def draw(self):

        frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width,
            height=self.height,
            topPadding=Spacing.Padding,
            bottomPadding=Spacing.Padding,
            rightPadding=Spacing.Padding,
            leftPadding=Spacing.Padding,
            showBoundary=self.debug_flag,
        )

        frame.addFromList(self.story, self.canv)
