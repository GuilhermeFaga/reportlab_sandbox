from reportlab.lib.styles import StyleSheet1, ParagraphStyle


from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

from src.enums import Poppins, Colors


class CustomStyleSheet(StyleSheet1):
    font = Poppins

    def __init__(self):
        super().__init__()

        registerFont(TTFont(Poppins.Regular, Poppins.RegularPath))
        registerFont(TTFont(Poppins.Bold, Poppins.BoldPath))
        registerFont(TTFont(Poppins.Italic, Poppins.ItalicPath))
        registerFont(TTFont(Poppins.BoldItalic, Poppins.BoldItalicPath))

        registerFontFamily(
            Poppins.Regular,
            normal=Poppins.Regular,
            bold=Poppins.Bold,
            italic=Poppins.Italic,
            boldItalic=Poppins.BoldItalic,
        )

        self.add(
            ParagraphStyle(
                name="Title",
                fontName=Poppins.Bold,
                fontSize=12,
            )
        )
        self.add(
            ParagraphStyle(
                name="Subtitle",
                fontName=Poppins.Bold,
                fontSize=10,
            )
        )
        self.add(
            ParagraphStyle(
                name="Body",
                fontName=Poppins.Regular,
                fontSize=9,
            )
        )
        self.add(
            ParagraphStyle(
                name="Caption",
                fontName=Poppins.Regular,
                fontSize=8,
            )
        )
        self.add(
            ParagraphStyle(
                name="Caption_70",
                fontName=Poppins.Regular,
                fontSize=8,
                textColor=Colors.Black_70,
            )
        )

    @property
    def Title(self) -> ParagraphStyle:
        return self["Title"]

    @property
    def Subtitle(self) -> ParagraphStyle:
        return self["Subtitle"]

    @property
    def Body(self) -> ParagraphStyle:
        return self["Body"]

    @property
    def Caption(self) -> ParagraphStyle:
        return self["Caption"]

    @property
    def Caption_70(self) -> ParagraphStyle:
        return self["Caption_70"]
