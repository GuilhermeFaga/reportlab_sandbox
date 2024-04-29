from src.types.misc import DictKey


class TableData:
    def __init__(
        self,
        columns: dict[DictKey, str],
        nested_fields: dict[DictKey, str],
        data: list[dict[str, str]],
    ):
        self.columns = columns
        self.nested_fields = nested_fields
        self.data = data

    @property
    def matrix(self) -> list[list]:
        return [
            [self.columns[key] for key in self.columns],
            *[[row[key] for key in self.columns] for row in self.data],
        ]
