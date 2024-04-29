from reportlab.platypus import Flowable, Paragraph, Frame, Spacer, Table

from src.primitives.list import ListPrimitive, ListData

from src.types.components import TableData
from src.styles.stylesheet import CustomStyleSheet

from src.enums import Spacing


class TablePrimitive(Flowable):

    def __init__(self, table_data: TableData, styles=CustomStyleSheet(), debug_flag=0):
        self.table_data = table_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        data = self.table_data.matrix
        header, rows = _formatHeaders(data[0]), data[1:]

        temp_table = Table(data=[header, *rows])

        temp_table.wrapOn(self.canv, self.max_width, self.max_height)

        # Get columns width from the table
        self.col_widths = temp_table._colWidths

        # Free table from memory
        del temp_table

        # Create a more complex table
        # Each row except the Header is a Flowable
        # These Flowables have a one row Table with data from table_data.columns
        # and if table_data.nested_fields is not empty,
        # a nested ListPrimitive with data from table_data.nested_fields

        # Pass the column width for all tables within the complex table
        # Wrap the complex table to get the height

        complex_data = [
            header,
            *[
                (
                    [
                        _ComplexRow(
                            row,
                            table_data=self.table_data,
                            col_widths=self.col_widths,
                            row_index=i,
                            styles=self.styles,
                        )
                    ]
                )
                for i, row in enumerate(rows)
            ],
        ]

        self.table = Table(complex_data, colWidths=self.col_widths)

        self.table.wrapOn(self.canv, self.max_width, self.max_height)

        self.height = self.table._height

        return (self.max_width, self.height)

    def draw(self):

        self.table.drawOn(self.canv, 0, 0)


def _ColHeader(text: str, styles=CustomStyleSheet()):
    return Paragraph(text, styles.Subtitle)


def _formatHeaders(row: list):
    return [_ColHeader(cell) for cell in row]


class _ComplexRow(Flowable):

    def __init__(
        self,
        row,
        table_data: TableData,
        col_widths,
        row_index,
        styles=CustomStyleSheet(),
    ):
        self.row = row
        self.table_data = table_data
        self.col_widths = col_widths
        self.row_index = row_index
        self.styles = styles

    def wrap(self, aW, aH):
        self.max_width = sum(self.col_widths)
        self.max_height = aH

        self.story: list[Flowable] = []

        self.table = Table(
            data=[self.row],
            colWidths=self.col_widths,
        )
        self.table.wrapOn(self.canv, self.max_width, self.max_height)

        self.height = self.table._height

        self.story.append(self.table)

        if self.table_data.nested_fields:
            self.list_primitive = ListPrimitive(
                ListData(
                    items=self.table_data.data[self.row_index],
                    fields=self.table_data.nested_fields,
                ),
                styles=self.styles,
            )
            self.list_primitive.wrapOn(self.canv, self.max_width, self.max_height)

            self.height += self.list_primitive.height

            self.story.append(self.table)

        return (self.max_width, self.height)

    def draw(self):

        frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width - Spacing.Gap,
            height=self.height,
            topPadding=0,
            bottomPadding=0,
            rightPadding=-Spacing.Gap,
            leftPadding=-Spacing.Gap,
            showBoundary=0,
        )

        frame.addFromList(self.story, self.canv)
