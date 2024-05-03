from src.types.misc import DictKey


class TableData:
    def __init__(
        self,
        columns: dict[DictKey, str],
        data: list[dict[str, str]],
        nested_fields: dict[DictKey, str] = {},
        overview: dict[str, str] = {},
    ):
        self.columns = columns
        self.data = data
        self.nested_fields = nested_fields
        self.overview = overview

    @property
    def matrix(self) -> list[list]:
        return [
            [self.columns[key] for key in self.columns],
            *[[row[key] for key in self.columns] for row in self.data],
        ]
