from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Flowable,
    Paragraph,
    Spacer,
)
from reportlab.pdfgen.canvas import Canvas

from src.enums import Spacing
from src.styles.stylesheet import CustomStyleSheet


class HeaderData:

    def __init__(
        self,
        category_name: str = "",
        product_name: str = "",
        entity_name: str = "",
        entity_id: str = "",
        date_time: str = "",
        protocol: str = "",
        pagination_template: str = "Página %s de %s",
        total_pages: int = 0,
    ):
        self.category_name = category_name
        self.product_name = product_name
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.date_time = date_time
        self.protocol = protocol
        self.pagination_template = pagination_template
        self.total_pages = total_pages


def Header(
    canvas: Canvas,
    doc: BaseDocTemplate,
    styles: CustomStyleSheet,
    header_data: HeaderData,
    debug_flag: int = 0,
):
    PAGE_WIDTH, PAGE_HEIGHT = canvas._pagesize

    left_story: list[Flowable] = []
    right_story: list[Flowable] = []

    left_frame = Frame(
        id="header",
        x1=Spacing.SafeMargin,
        y1=PAGE_HEIGHT - Spacing.SafeMargin - Spacing.HeaderHeight,
        width=PAGE_WIDTH / 2 - Spacing.SafeMargin,
        height=Spacing.HeaderHeight,
        topPadding=Spacing.Padding,
        bottomPadding=Spacing.Padding,
        rightPadding=Spacing.Padding,
        leftPadding=Spacing.Padding,
        showBoundary=debug_flag,
    )

    right_frame = Frame(
        id="header",
        x1=PAGE_WIDTH / 2,
        y1=PAGE_HEIGHT - Spacing.SafeMargin - Spacing.HeaderHeight,
        width=PAGE_WIDTH / 2 - Spacing.SafeMargin,
        height=Spacing.HeaderHeight,
        topPadding=Spacing.Padding,
        bottomPadding=Spacing.Padding,
        rightPadding=Spacing.Padding,
        leftPadding=Spacing.Padding,
        showBoundary=debug_flag,
    )

    left_story.append(Paragraph(header_data.category_name, styles.Title))
    left_story.append(Paragraph(header_data.product_name, styles.Subtitle))
    left_story.append(
        Paragraph(
            "%s (%s)" % (header_data.entity_name, header_data.entity_id),
            styles.Body,
        )
    )

    left_frame.addFromList(left_story, canvas)

    right_story.append(Paragraph(header_data.date_time, styles.Body_Right))
    right_story.append(Paragraph(header_data.protocol, styles.Caption_70_Right))
    right_story.append(Spacer(1, Spacing.Gap))
    right_story.append(
        Paragraph(
            header_data.pagination_template % (doc.page, header_data.total_pages),
            styles.Caption_70_Right,
        )
    )

    right_frame.addFromList(right_story, canvas)
