from src.pdf_builder import PDFBuilder

from src.components.header import HeaderData
from src.components.list import List
from src.components.icon_card_list import IconCardList
from src.components.score import Score
from src.components.gauge_card_list import GaugeCardList
from src.components.table import Table

from src.enums import Colors, SvgPath

from src.types.components import (
    ListData,
    IconCardData,
    ScoreData,
    ScoreRangeData,
    ScoreNotValidData,
    GaugeCardListData,
    GaugeCardGroupData,
    GaugeCardData,
    TableData,
)
from src.types.misc import DictKey


class RelatorioPositivo:

    def __init__(self):
        reportlab_debug = 0

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
                DictKey("cnpj"): "CNPJ",
                DictKey("situacao"): "Situação",
                DictKey("razao_social"): "Razão Social",
                DictKey("atividade_principal"): "Atividade Principal",
                DictKey("endereco"): "Endereço",
                DictKey("bairro"): "Bairro",
                DictKey("cidade"): "Cidade",
                DictKey("cep"): "CEP",
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
                    title="Pontualidade de pagamento",
                    cards=[
                        GaugeCardData(
                            title="Pontualidade de pagamento",
                            description="Compromissos financeiros pagos em dia",
                            level=1,
                            level_text="Risco baixo",
                            color=Colors.Green,
                        ),
                        GaugeCardData(
                            title="Tempo de atraso",
                            description="Dívidas vencidas ou não pagas com atraso",
                            level=3,
                            level_text="Risco alto",
                            color=Colors.Red,
                        ),
                    ],
                ),
                GaugeCardGroupData(
                    title="Endividamento",
                    cards=[
                        GaugeCardData(
                            title="Quantidade de contratos em aberto",
                            description="Volume de contratos em aberto",
                            level=3,
                            level_text="Risco alto",
                            color=Colors.Red,
                        ),
                        GaugeCardData(
                            title="Uso de crédito emergencial",
                            description="Volumo de uso de crédito emergencial",
                            level=1,
                            level_text="Risco baixo",
                            color=Colors.Green,
                        ),
                    ],
                ),
                GaugeCardGroupData(
                    title="Relacionamento com o mercado",
                    cards=[
                        GaugeCardData(
                            title="Risco do perfil de contratação",
                            description="Uso de produtos de crédito de risco",
                            level=3,
                            level_text="Risco alto",
                            color=Colors.Red,
                        ),
                        GaugeCardData(
                            title="Quantidade de novas contratações",
                            description="Contratos de crédito nos últimos 12 meses",
                            level=1,
                            level_text="Risco baixo",
                            color=Colors.Green,
                        ),
                        GaugeCardData(
                            title="Perfil de relacionamento",
                            description="Relacionamentos com credores",
                            level=2,
                            level_text="Risco médio",
                            color=Colors.Orange,
                        ),
                    ],
                ),
            ]
        )

        table_data = TableData(
            columns={
                DictKey("data"): "Data",
                DictKey("descricao"): "Descrição",
                DictKey("usuario"): "Usuário",
                DictKey("protocolo"): "Protocolo",
            },
            nested_fields={
                DictKey("nested"): "Nested Field 1",
                DictKey("nested2"): "Nested Field 2",
                DictKey("nested3"): "Nested Field 3",
                DictKey("nested4"): "Nested Field 4",
            },
            overview={
                "Total de consultas": "20",
                "Consultas realizadas": "20",
            },
            data=[
                {
                    "data": "12/04/2024",
                    "descricao": "Consulta realizada",
                    "usuario": "Usuário",
                    "protocolo": "52023152-59018723807912038",
                    "nested": "Nested Field 1",
                    "nested2": "Nested Field 2",
                    "nested3": "Nested Field 3",
                    "nested4": "Nested Field 4",
                }
                for _ in range(20)
            ],
        )

        pdf = PDFBuilder("phello.pdf", header_data)

        pdf.add_flowable(
            List("Dados Cadastrais", list_data, debug_flag=reportlab_debug)
        )
        pdf.add_flowable(
            IconCardList("Resumo", icon_card_list, debug_flag=reportlab_debug)
        )
        pdf.add_flowable(Score("Score", score_data, debug_flag=reportlab_debug))
        pdf.add_flowable(
            GaugeCardList(
                "Indicadores de Negócio", gauge_card_list, debug_flag=reportlab_debug
            )
        )
        pdf.add_flowable(
            Table("Histórico de Consultas", table_data, debug_flag=reportlab_debug)
        )

        pdf.build()
