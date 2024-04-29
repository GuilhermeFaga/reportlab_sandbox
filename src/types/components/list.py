from src.types.misc import DictKey


class ListData:
    def __init__(self, items: dict[str, str], fields: dict[DictKey, str]):
        self.items = items
        self.fields = fields
