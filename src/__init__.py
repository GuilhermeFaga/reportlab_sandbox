from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Flowable,
    PageTemplate,
    Paragraph,
    Spacer,
    KeepTogether,
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm

from reportlab.pdfgen.canvas import Canvas

from src.styles.stylesheet import CustomStyleSheet

from src.enums import Spacing

import copy
import io


PAGE_WIDTH, PAGE_HEIGHT = A4

Title = "Hello world"
pageinfo = "platypus example"

reportlab_debug = 1


"""
ReportLab Platypus hierarchy:

* DocTemplates the outermost container for the document;
* PageTemplates specifications for layouts of pages of various kinds;
* Frames specifications of regions in pages that can contain flowing text or graphics;
* Flowables text or graphic elements that should be "flowed into the document 
(i.e. things like images, paragraphs and tables, 
but not things like page footers or fixed page graphics);
* pdfgen.Canvas the lowest level which ultimately receives the painting of 
the document from the other layers.
"""


styles = CustomStyleSheet()


class HeaderData:

    def __init__(
        self,
        category_name: str = "",
        product_name: str = "",
        entity_name: str = "",
        entity_id: str = "",
        date_time: str = "",
        protocol: str = "",
        page_info: str = "Página %s de %s",
    ):
        self.category_name = category_name
        self.product_name = product_name
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.date_time = date_time
        self.protocol = protocol
        self.page_info = page_info


total_pages = 0


class PDFBuilder:

    def __init__(self, filename: str, header_data: HeaderData = HeaderData()):
        self.filename = filename
        self.header_data = header_data

        frame_width = PAGE_WIDTH - 2 * Spacing.SafeMargin
        frame_height = (
            PAGE_HEIGHT - 2 * Spacing.SafeMargin - Spacing.HeaderHeight - Spacing.Gap
        )

        frame = Frame(
            id="normal",
            x1=Spacing.SafeMargin,
            y1=Spacing.SafeMargin,
            width=frame_width,
            height=frame_height,
            topPadding=Spacing.Padding,
            bottomPadding=Spacing.Padding,
            rightPadding=Spacing.Padding,
            leftPadding=Spacing.Padding,
            showBoundary=reportlab_debug,
        )

        pageTemplate = PageTemplate(
            frames=[frame],
            onPage=self.page_builder,
        )

        self.doc = BaseDocTemplate(
            filename=self.filename,
            pageTemplates=[pageTemplate],
            pagesize=A4,
            rightMargin=Spacing.SafeMargin,
            leftMargin=Spacing.SafeMargin,
            topMargin=Spacing.SafeMargin,
            bottomMargin=Spacing.SafeMargin,
            showBoundary=reportlab_debug,
        )

        self.story: list[Flowable] = []

    def page_builder(self, canvas: Canvas, doc: BaseDocTemplate):
        canvas.saveState()
        self.build_header(canvas, doc)
        canvas.restoreState()

    def build_header(self, canvas: Canvas, doc: BaseDocTemplate):
        global total_pages
        total_pages = max(total_pages, doc.page)

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
            showBoundary=reportlab_debug,
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
            showBoundary=reportlab_debug,
        )

        left_story.append(Paragraph(self.header_data.category_name, styles.Title))
        left_story.append(Paragraph(self.header_data.product_name, styles.Subtitle))
        left_story.append(
            Paragraph(
                "%s (%s)" % (self.header_data.entity_name, self.header_data.entity_id),
                styles.Body,
            )
        )

        left_frame.addFromList(left_story, canvas)

        right_story.append(Paragraph(self.header_data.date_time, styles.Body_Right))
        right_story.append(
            Paragraph(self.header_data.protocol, styles.Caption_70_Right)
        )
        right_story.append(Spacer(1, Spacing.Gap))
        right_story.append(
            Paragraph(
                self.header_data.page_info % (doc.page, total_pages),
                styles.Caption_70_Right,
            )
        )

        right_frame.addFromList(right_story, canvas)

    def generate_test_data(self, limit: int = 15):
        for i in range(limit):
            bogustext = ("This is Paragraph number %s. " % i) * 20
            p = Paragraph(bogustext, styles.Body)
            self.story.append(KeepTogether([p]))

        self.story.append(Spacer(1, Spacing.Gap))

    def build(self):
        with io.BytesIO() as out:
            doc = copy.deepcopy(self.doc)
            doc.build(copy.deepcopy(self.story), out)

        self.doc.build(self.story)

        global total_pages
        total_pages = 0


def main():

    header_data = HeaderData(
        category_name="Análise de crédito",
        product_name="Relatório Positivo",
        entity_name="RAZÃO SOCIAL",
        entity_id="00.000.000/0001-00",
        date_time="12/04/2024 10:00",
        protocol="52023152-59018723807912038",
    )

    pdf = PDFBuilder("phello.pdf", header_data)
    pdf.generate_test_data()
    pdf.build()


if __name__ == "__main__":
    main()
