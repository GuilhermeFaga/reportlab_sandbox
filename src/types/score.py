from src.enums import Colors


class ScoreNotValidData:
    def __init__(self, color: Colors, aux_template, description: str, aux_value: str):
        self.color = color
        self.aux_template = aux_template
        self.description = description
        self.aux_value = aux_value


class ScoreRangeData:
    def __init__(self, max_score: int, color: Colors, description: str, aux_value: str):
        self.max_score = max_score
        self.color = color
        self.description = description
        self.aux_value = aux_value


class ScoreData:
    def __init__(
        self,
        score: int,
        min_score: int,
        aux_title: str,
        aux_template: str,
        aux_color: Colors,
        not_valid_data: ScoreNotValidData,
        ranges: list[ScoreRangeData],
    ):
        self.score = score
        self.min_score = min_score
        self.aux_title = aux_title
        self.aux_template = aux_template
        self.aux_color = aux_color
        self.not_valid_data = not_valid_data
        self.ranges = ranges

    @property
    def current_range(self) -> ScoreRangeData:
        for range_data in self.ranges:
            if self.score < range_data.max_score:
                return range_data
        return self.ranges[-1]

    @property
    def is_score_valid(self):
        return self.score > self.min_score
