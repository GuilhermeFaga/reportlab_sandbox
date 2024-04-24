from reportlab.platypus import Flowable, Frame, Paragraph
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.styles import ParagraphStyle

from src.enums import Colors, Spacing
from src.styles.stylesheet import CustomStyleSheet
from src.types import ScoreData, ScoreRangeData


class ScoreTextPrimitive(Flowable):

    def __init__(
        self, score_data: ScoreData, styles=CustomStyleSheet(), debug_flag: int = 0
    ):
        self.score_data = score_data
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.aux_title_para = Paragraph(
            text=self.score_data.aux_title,
            style=self.styles.Subtitle,
        )
        self.aux_value_flow = _AuxValue(
            score_data=self.score_data,
            styles=self.styles,
            debug_flag=self.debug_flag,
        )

        aux_description_text = (
            self.score_data.aux_template
            % self.score_data.current_range.aux_value.lower()
        )

        if not self.score_data.is_score_valid:
            aux_description_text = self.score_data.not_valid_data.aux_template

        self.aux_description_para = Paragraph(
            text=aux_description_text,
            style=self.styles.Body,
        )

        self.aux_title_para.wrapOn(self.canv, self.max_width, 1)
        self.aux_value_flow.wrapOn(self.canv, self.max_width, 1)
        self.aux_description_para.wrapOn(self.canv, self.max_width, 1)

        self.height = (
            self.aux_title_para.height
            + self.aux_title_para.getSpaceAfter()
            + self.aux_value_flow.height
            + self.aux_description_para.getSpaceBefore()
            + self.aux_description_para.height
        )

        return (self.max_width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        frame = Frame(
            x1=0,
            y1=0,
            width=self.max_width,
            height=self.height,
            topPadding=0,
            bottomPadding=0,
            rightPadding=0,
            leftPadding=0,
            showBoundary=self.debug_flag,
        )

        self.aux_title_para.debug = self.debug_flag
        self.aux_description_para.debug = self.debug_flag

        frame.addFromList(
            [
                self.aux_title_para,
                self.aux_value_flow,
                self.aux_description_para,
            ],
            canvas,
        )


class _AuxValue(Flowable):

    def __init__(
        self,
        score_data: ScoreData,
        styles=CustomStyleSheet(),
        debug_flag: int = 0,
    ):
        self.score_data = score_data
        self.current_range = self.score_data.current_range
        self.styles = styles
        self.debug_flag = debug_flag

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        self.aux_value_color = self.current_range.color
        aux_value_text = self.current_range.aux_value

        if not self.score_data.is_score_valid:
            aux_value_text = self.score_data.not_valid_data.aux_value
            self.aux_value_color = self.score_data.not_valid_data.color

        aux_value_styles = {
            **self.styles.Subtitle_Center.__dict__,
            "textColor": Colors.getTextColor(self.aux_value_color).value,
        }
        self.aux_value_para = Paragraph(
            text=aux_value_text,
            style=ParagraphStyle(**aux_value_styles),
        )

        self.aux_value_para.wrapOn(self.canv, self.max_width, 1)

        self.width = self.aux_value_para._width_max + Spacing.Gap * 2
        self.height = self.aux_value_para.height + Spacing.Padding * 2

        return (self.width, self.height)

    def draw(self):
        canvas: Canvas = self.canv

        frame = Frame(
            x1=0,
            y1=0,
            width=self.width,
            height=self.height,
            topPadding=Spacing.Padding,
            bottomPadding=Spacing.Padding,
            rightPadding=Spacing.Gap,
            leftPadding=Spacing.Gap,
            showBoundary=self.debug_flag,
        )

        self.aux_value_para.debug = self.debug_flag

        canvas.setFillColor(self.aux_value_color.value)
        canvas.setStrokeAlpha(0)

        if self.debug_flag:
            canvas.setFillAlpha(0.5)
            canvas.setStrokeAlpha(1)

        canvas.rect(
            x=0,
            y=0,
            width=self.width,
            height=self.height,
            fill=1,
        )

        frame.addFromList([self.aux_value_para], canvas)
