from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib import enums

from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

from src.enums import Poppins, Colors


class CustomStyleSheet(StyleSheet1):

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

        title_style = {
            "name": "Title",
            "fontName": Poppins.Bold,
            "fontSize": 12,
            "spaceBefore": 8.0,
            "spaceAfter": 8.0,
        }

        subtitle_style = {
            "name": "Subtitle",
            "fontName": Poppins.Bold,
            "fontSize": 10,
            "spaceBefore": 5.0,
            "spaceAfter": 5.0,
        }

        body_style = {
            "name": "Body",
            "fontName": Poppins.Regular,
            "fontSize": 9,
            "spaceBefore": 5.0,
            "spaceAfter": 5.0,
        }

        caption_style = {
            "name": "Caption",
            "fontName": Poppins.Regular,
            "fontSize": 8,
        }

        caption_70_style = {
            "name": "Caption_70",
            "fontName": Poppins.Regular,
            "fontSize": 8,
            "textColor": Colors.Black_70,
        }

        styles = [
            title_style,
            subtitle_style,
            body_style,
            caption_style,
            caption_70_style,
        ]

        for style in styles:
            self.add(ParagraphStyle(**style))
            self.add(
                ParagraphStyle(
                    **{
                        **style,
                        "name": style["name"] + "_Center",
                        "alignment": enums.TA_CENTER,
                    }
                )
            )
            self.add(
                ParagraphStyle(
                    **{
                        **style,
                        "name": style["name"] + "_Right",
                        "alignment": enums.TA_RIGHT,
                    }
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

    @property
    def Title_Center(self) -> ParagraphStyle:
        return self["Title_Center"]

    @property
    def Subtitle_Center(self) -> ParagraphStyle:
        return self["Subtitle_Center"]

    @property
    def Body_Center(self) -> ParagraphStyle:
        return self["Body_Center"]

    @property
    def Caption_Center(self) -> ParagraphStyle:
        return self["Caption_Center"]

    @property
    def Caption_70_Center(self) -> ParagraphStyle:
        return self["Caption_70_Center"]

    @property
    def Title_Right(self) -> ParagraphStyle:
        return self["Title_Right"]

    @property
    def Subtitle_Right(self) -> ParagraphStyle:
        return self["Subtitle_Right"]

    @property
    def Body_Right(self) -> ParagraphStyle:
        return self["Body_Right"]

    @property
    def Caption_Right(self) -> ParagraphStyle:
        return self["Caption_Right"]

    @property
    def Caption_70_Right(self) -> ParagraphStyle:
        return self["Caption_70_Right"]
