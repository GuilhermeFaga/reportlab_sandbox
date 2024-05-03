from reportlab.platypus import Flowable, Frame, Spacer

from src.primitives.title import TitlePrimitive
from src.primitives.list import ListPrimitive, ListData
from src.primitives.table import TablePrimitive, TableData

from src.enums import Spacing

from src.types.misc import DictKey


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

        self.list_primitive = None
        if self.table_data.overview:
            overview_data = ListData(
                items=self.table_data.overview,
                fields={DictKey(key): key for key in self.table_data.overview.keys()},
            )
            self.list_primitive = ListPrimitive(
                overview_data, debug_flag=self.debug_flag
            )

            self.list_primitive.wrapOn(self.canv, self.max_width, 1)

            self.height += self.list_primitive.height + Spacing.Gap

        return (self.max_width, self.height)

    def split(self, aW, aH):
        header_height, first_row_height, *_ = self.table_primitive.table._rowHeights
        overview_height = (
            self.list_primitive.height + Spacing.Gap if self.list_primitive else 0
        )
        min_height = (
            self.title_primitive.height
            + Spacing.Gap
            + overview_height
            + int(header_height or 0)
            + int(first_row_height or 0)
        )

        if aH < min_height:
            return []

        return [
            self.title_primitive,
            Spacer(1, Spacing.Gap),
            self.list_primitive,
            Spacer(1, Spacing.Gap) if self.list_primitive else None,
            *self.table_primitive.split(aW, aH),
        ]

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
