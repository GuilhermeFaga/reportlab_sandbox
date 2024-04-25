from src.enums import Colors


class GaugeCardData:
    def __init__(
        self, title: str, description: str, level: int, level_text: str, color: Colors
    ):
        self.title = title
        self.description = description
        self.level = level
        self.level_text = level_text
        self.color = color


class GaugeCardGroupData:
    def __init__(self, title: str, cards: list[GaugeCardData]):
        self.title = title
        self.cards = cards


class GaugeCardListData:
    def __init__(self, groups: list[GaugeCardGroupData]):
        self.groups = groups
