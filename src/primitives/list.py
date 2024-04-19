from reportlab.platypus import Flowable, Paragraph, Frame, Spacer
from reportlab.pdfgen.canvas import Canvas

from src.enums import Spacing
from src.styles.stylesheet import CustomStyleSheet

from math import ceil
from typing import Any, Final


field_template: Final[str] = "%s:"

padding_x: Final[int] = Spacing.Padding
padding_y: Final[int] = Spacing.Padding


class ListData:
    def __init__(self, items: dict[str, Any], fields: dict[str, Any]):
        self.items = items
        self.fields = fields


class List(Flowable):

    def __init__(
        self,
        list_data: ListData,
        styles: CustomStyleSheet = CustomStyleSheet(),
    ):
        self.list_data = list_data
        self.styles = styles

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.max_field_width_left = 0
        self.max_field_width_right = 0

        index = 0
        for key, value in self.list_data.fields.items():
            field_para = Paragraph(field_template % value, self.styles.Body_Bold_Right)
            field_para.wrapOn(self.canv, self.max_width, 1)

            if index % 2 == 0:
                if field_para._width_max > self.max_field_width_left:
                    self.max_field_width_left = field_para._width_max
            else:
                if field_para._width_max > self.max_field_width_right:
                    self.max_field_width_right = field_para._width_max

            index += 1
            del field_para

        self.accumulated_height_left = 0
        self.accumulated_height_right = 0

        self.accumulated_height = 0

        index = 0
        for key, value in self.list_data.fields.items():
            row_value = self.list_data.items.get(key, "")
            value_para = Paragraph(str(row_value), self.styles.Body)

            if index % 2 == 0:
                value_para.wrapOn(
                    self.canv,
                    self.max_width / 2 - self.max_field_width_left - Spacing.Padding,
                    1,
                )
                self.accumulated_height_left += value_para.height
            else:
                value_para.wrapOn(
                    self.canv,
                    self.max_width / 2
                    - self.max_field_width_right
                    - Spacing.Padding
                    - padding_x * 2,
                    1,
                )
                self.accumulated_height_right += value_para.height

            index += 1
            del value_para

        spacers_count = max(1, len(self.list_data.fields) / 2 - 1)

        self.accumulated_height_left += ceil(spacers_count) * Spacing.Padding
        self.accumulated_height_right += ceil(spacers_count) * Spacing.Padding

        self.accumulated_height = (
            max(self.accumulated_height_left, self.accumulated_height_right)
            + padding_y * 2
        )

        return (self.max_width, self.accumulated_height)

    def draw(self):
        canvas: Canvas = self.canv

        left_story: list[Flowable] = []
        right_story: list[Flowable] = []

        left_frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width / 2,
            height=self.accumulated_height,
            topPadding=padding_y,
            bottomPadding=padding_y,
            leftPadding=padding_x,
            rightPadding=padding_x,
            showBoundary=0,
        )

        right_frame = Frame(
            x1=self.max_width / 2,
            y1=0,
            width=self.max_width / 2,
            height=self.accumulated_height,
            topPadding=padding_y,
            bottomPadding=padding_y,
            leftPadding=padding_x,
            rightPadding=padding_x,
            showBoundary=0,
        )

        index = 0
        for key, value in self.list_data.fields.items():
            row_field = value
            row_value = self.list_data.items.get(key, "")

            if index % 2 == 0:
                row = ListRow(
                    field=row_field,
                    value=row_value,
                    field_width=self.max_field_width_left,
                    styles=self.styles,
                )
                left_story.append(row)
                left_story.append(Spacer(1, Spacing.Padding))
            else:
                row = ListRow(
                    field=row_field,
                    value=row_value,
                    field_width=self.max_field_width_right,
                    styles=self.styles,
                )
                right_story.append(row)
                right_story.append(Spacer(1, Spacing.Padding))

            index += 1

        left_frame.addFromList(left_story, canvas)
        right_frame.addFromList(right_story, canvas)


class ListRow(Flowable):

    def __init__(
        self,
        field: str,
        value: str,
        field_width: float,
        styles: CustomStyleSheet = CustomStyleSheet(),
    ):
        self.field = field
        self.value = str(value)
        self.field_width = field_width
        self.styles = styles

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.field_para = Paragraph(
            field_template % self.field, self.styles.Body_Bold_Right
        )
        self.field_para.wrapOn(self.canv, self.field_width, 1)

        self.value_para = Paragraph(self.value, self.styles.Body)
        self.value_para.wrapOn(
            self.canv, self.max_width - self.field_width - Spacing.Padding, 1
        )

        return (self.max_width, self.value_para.height)

    def draw(self):
        self.field_para.drawOn(
            self.canv, 0, self.value_para.height - self.field_para.height
        )
        self.value_para.drawOn(self.canv, self.field_width + Spacing.Padding, 0)
