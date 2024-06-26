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
from reportlab.pdfgen.canvas import Canvas

from src.components.header import Header, HeaderData

from src.styles.stylesheet import CustomStyleSheet
from src.enums import Spacing

import copy
import io


PAGE_WIDTH, PAGE_HEIGHT = A4

reportlab_debug = 0


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
            topPadding=0,
            bottomPadding=0,
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

        self.header_data.total_pages = total_pages
        Header(canvas, doc, self.header_data, debug_flag=reportlab_debug)

    def add_flowable(self, flowable: Flowable):
        self.story.append(flowable)
        self.story.append(Spacer(1, Spacing.Gap * 2))

    def build(self):
        with io.BytesIO() as out:
            doc = copy.deepcopy(self.doc)
            doc.build(copy.deepcopy(self.story), out)

        self.doc.build(self.story)

        global total_pages
        total_pages = 0
