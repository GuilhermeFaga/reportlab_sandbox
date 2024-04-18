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


def Header(canvas: Canvas, doc: BaseDocTemplate):
    story: list[Flowable] = []
    frame = Frame(
        id="header",
        x1=Spacing.SafeMargin,
        y1=PAGE_HEIGHT - Spacing.SafeMargin - Spacing.HeaderHeight,
        width=PAGE_WIDTH - 2 * Spacing.SafeMargin,
        height=Spacing.HeaderHeight,
        topPadding=Spacing.Padding,
        bottomPadding=Spacing.Padding,
        rightPadding=Spacing.Padding,
        leftPadding=Spacing.Padding,
        showBoundary=reportlab_debug,
    )
    story.append(Paragraph(Title, styles.Title))
    story.append(Paragraph("Page %d %s" % (doc.page, pageinfo), styles.Caption_70))
    frame.addFromList(story, canvas)


def Page(canvas: Canvas, doc: BaseDocTemplate):
    canvas.saveState()
    Header(canvas, doc)
    canvas.restoreState()


def main():

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
        onPage=Page,
    )

    doc = BaseDocTemplate(
        filename="phello.pdf",
        pageTemplates=[pageTemplate],
        pagesize=A4,
        rightMargin=Spacing.SafeMargin,
        leftMargin=Spacing.SafeMargin,
        topMargin=Spacing.SafeMargin,
        bottomMargin=Spacing.SafeMargin,
        showBoundary=reportlab_debug,
    )

    story: list[Flowable] = []

    for i in range(15):
        bogustext = ("This is Paragraph number %s. " % i) * 20
        p = Paragraph(bogustext, styles.Body)
        story.append(KeepTogether([p]))
        story.append(Spacer(1, Spacing.Gap))

    doc.build(story)


if __name__ == "__main__":
    main()
