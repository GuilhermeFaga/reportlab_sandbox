from reportlab.platypus import Flowable, Paragraph, Frame, Table
from reportlab.pdfgen.canvas import Canvas

from src.primitives.list import ListPrimitive, ListData

from src.types.components import TableData
from src.styles.stylesheet import CustomStyleSheet

from src.enums import Spacing, Colors


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

        self.col_widths = temp_table._colWidths

        del temp_table

        complex_rows = (
            [
                _ComplexRow(
                    row,
                    table_data=self.table_data,
                    col_widths=self.col_widths,
                    row_index=i,
                    styles=self.styles,
                    debug_flag=self.debug_flag,
                )
            ]
            for i, row in enumerate(rows)
        )

        complex_data = [header, *complex_rows]

        self.table = Table(
            complex_data,
            colWidths=self.col_widths,
            repeatRows=1,
        )

        self.table.wrapOn(self.canv, self.max_width, self.max_height)

        self.height = self.table._height

        return (self.max_width, self.height)

    def split(self, aW, aH):
        return self.table.split(aW, aH)

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
        debug_flag=0,
    ):
        self.row = row
        self.table_data = table_data
        self.col_widths = col_widths
        self.row_index = row_index
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = sum(self.col_widths)
        self.max_height = aH

        self.story: list[Flowable] = []

        self.table = Table(
            data=[self.row],
            colWidths=self.col_widths,
        )
        self.table.wrapOn(self.canv, self.max_width - Spacing.Gap, self.max_height)

        self.height = self.table._height

        self.story.append(self.table)

        if self.table_data.nested_fields:
            self.list_primitive = ListPrimitive(
                ListData(
                    items=self.table_data.data[self.row_index],
                    fields=self.table_data.nested_fields,
                ),
                styles=self.styles,
                debug_flag=self.debug_flag,
            )
            self.list_primitive.wrapOn(
                self.canv, self.max_width - Spacing.Gap, self.max_height
            )

            self.height += self.list_primitive.height

            self.story.append(self.list_primitive)

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width - Spacing.Gap,
            height=self.height,
            topPadding=0,
            bottomPadding=0,
            rightPadding=Spacing.Gap,
            leftPadding=Spacing.Gap,
            showBoundary=self.debug_flag,
        )

        if self.row_index % 2 == 0:
            canvas.setFillColor(Colors.Gray.value)
            canvas.setStrokeAlpha(0)
            canvas.rect(
                x=-Spacing.Padding / 2,
                y=-Spacing.Padding / 2,
                width=self.max_width - Spacing.Padding,
                height=self.height + Spacing.Padding,
                fill=1,
            )

        frame.addFromList(self.story, canvas)
