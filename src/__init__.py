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
from src.components.list import List, ListData
from src.components.icon_card_list import IconCardList, IconCardData
from src.components.score import Score
from src.components.gauge_card_list import GaugeCardList

from src.styles.stylesheet import CustomStyleSheet
from src.enums import Colors, Spacing, SvgPath

from src.types import (
    ScoreData,
    ScoreRangeData,
    ScoreNotValidData,
    GaugeCardListData,
    GaugeCardGroupData,
    GaugeCardData,
)

import copy
import io


PAGE_WIDTH, PAGE_HEIGHT = A4

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
        date_time="12/04/2024 - 10:00",
        protocol="52023152-59018723807912038",
    )

    list_data = ListData(
        fields={
            "cnpj": "CNPJ",
            "situacao": "Situação",
            "razao_social": "Razão Social",
            "atividade_principal": "Atividade Principal",
            "endereco": "Endereço",
            "bairro": "Bairro",
            "cidade": "Cidade",
            "cep": "CEP",
        },
        items={
            "cnpj": "00.000.000/0001-00",
            "situacao": "Ativa",
            "razao_social": "RAZÃO SOCIAL",
            "atividade_principal": "ATIVIDADE PRINCIPAL",
            "endereco": "ENDEREÇO",
            "bairro": "BAIRRO",
            "cidade": "CIDADE",
            "cep": "00000-000",
        },
    )

    icon_card_list: list[IconCardData] = [
        IconCardData(
            title="Situação",
            description="Possui Restrições",
            icon=SvgPath.Warning,
            color=Colors.Orange,
        ),
        IconCardData(
            title="Protestos",
            description="R$127K",
            icon=SvgPath.Error,
            color=Colors.Red,
        ),
        IconCardData(
            title="Negativações",
            description="R$104K",
            icon=SvgPath.Error,
            color=Colors.Red,
        ),
        IconCardData(
            title="Ações Judiciais",
            description="R$0",
            icon=SvgPath.Check,
            color=Colors.Green,
        ),
        IconCardData(
            title="Cheques sem Fundos",
            description="0",
            icon=SvgPath.Check,
            color=Colors.Green,
        ),
    ]

    score_data = ScoreData(
        score=950,
        min_score=300,
        aux_title="Risco de Crédito",
        aux_template="""De acordo com o perfil do CNPJ consultado e seu principal sócio, o risco de 
        não pagamento dos compromissos financeiros da empresa é estatisticamente %s.""",
        not_valid_data=ScoreNotValidData(
            color=Colors.Gray,
            aux_template="Este consumidor não possui informacões suficientes disponíveis para calcular o Score.",
            description="Não se aplica",
            aux_value="Não se aplica",
        ),
        ranges=[
            ScoreRangeData(
                max_score=400,
                color=Colors.Red,
                description="Muito Ruim",
                aux_value="Muito Alto",
            ),
            ScoreRangeData(
                max_score=500,
                color=Colors.Red,
                description="Muito Ruim",
                aux_value="Muito Alto",
            ),
            ScoreRangeData(
                max_score=600,
                color=Colors.Orange,
                description="Ruim",
                aux_value="Alto",
            ),
            ScoreRangeData(
                max_score=700,
                color=Colors.Orange,
                description="Bom",
                aux_value="Médio",
            ),
            ScoreRangeData(
                max_score=800,
                color=Colors.Orange,
                description="Bom",
                aux_value="Médio",
            ),
            ScoreRangeData(
                max_score=900,
                color=Colors.Green,
                description="Ótimo",
                aux_value="Baixo",
            ),
            ScoreRangeData(
                max_score=1000,
                color=Colors.Green,
                description="Ótimo",
                aux_value="Baixo",
            ),
        ],
    )

    gauge_card_list = GaugeCardListData(
        groups=[
            GaugeCardGroupData(
                title="Grupo 1",
                cards=[
                    GaugeCardData(
                        title="Card 1",
                        description="Descrição do Card 1",
                        level=1,
                        level_text="Baixo",
                        color=Colors.Green,
                    ),
                    GaugeCardData(
                        title="Card 2",
                        description="Descrição do Card 2",
                        level=2,
                        level_text="Médio",
                        color=Colors.Orange,
                    ),
                    GaugeCardData(
                        title="Card 3",
                        description="Descrição do Card 3",
                        level=3,
                        level_text="Alto",
                        color=Colors.Red,
                    ),
                ],
            ),
            GaugeCardGroupData(
                title="Grupo 2",
                cards=[
                    GaugeCardData(
                        title="Card 1",
                        description="Descrição do Card 1",
                        level=1,
                        level_text="Baixo",
                        color=Colors.Green,
                    ),
                    GaugeCardData(
                        title="Card 2",
                        description="Descrição do Card 2",
                        level=2,
                        level_text="Médio",
                        color=Colors.Orange,
                    ),
                    GaugeCardData(
                        title="Card 3",
                        description="Descrição do Card 3",
                        level=3,
                        level_text="Alto",
                        color=Colors.Red,
                    ),
                ],
            ),
        ]
    )

    pdf = PDFBuilder("phello.pdf", header_data)

    pdf.add_flowable(List("Dados Cadastrais", list_data, debug_flag=reportlab_debug))
    pdf.add_flowable(IconCardList("Resumo", icon_card_list, debug_flag=reportlab_debug))
    pdf.add_flowable(Score("Score", score_data, debug_flag=reportlab_debug))
    pdf.add_flowable(
        GaugeCardList(
            "Indicadores de Negócio", gauge_card_list, debug_flag=reportlab_debug
        )
    )

    pdf.generate_test_data()
    pdf.build()


if __name__ == "__main__":
    main()
