from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfgen.canvas import Canvas

PAGE_WIDTH, PAGE_HEIGHT = A4

Title = "Hello world"
pageinfo = "platypus example"


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


def myFirstPage(canvas: Canvas, doc: SimpleDocTemplate):
    canvas.saveState()

    canvas.setFont("Times-Bold", 16)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, Title)

    canvas.setFont("Times-Roman", 9)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)

    canvas.restoreState()


def myLaterPages(canvas: Canvas, doc: SimpleDocTemplate):
    canvas.saveState()

    canvas.setFont("Times-Roman", 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))

    canvas.restoreState()


def main():
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate("phello.pdf", pagesize=A4)

    Story = [Spacer(1, 2 * inch)]
    style = styles["Normal"]

    for i in range(100):
        bogustext = ("This is Paragraph number %s. " % i) * 20
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(1, 0.2 * inch))

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


if __name__ == "__main__":
    main()
