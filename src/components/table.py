from reportlab.platypus import Flowable, Frame, Spacer

from src.primitives.title import TitlePrimitive
from src.primitives.table import TablePrimitive, TableData

from src.enums import Spacing


class Table(Flowable):

    def __init__(self, title: str, table_data: TableData, debug_flag: int = 0):
        self.title = title
        self.table_data = table_data
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.title_primitive = TitlePrimitive(self.title, debug_flag=self.debug_flag)
        self.table_primitive = TablePrimitive(
            self.table_data, debug_flag=self.debug_flag
        )

        self.title_primitive.wrapOn(self.canv, self.max_width, 1)
        self.table_primitive.wrapOn(self.canv, self.max_width, 1)

        self.height = (
            self.title_primitive.height + self.table_primitive.height + Spacing.Gap
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
                self.table_primitive,
            ],
            self.canv,
        )
