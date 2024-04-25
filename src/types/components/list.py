from typing import Any


class ListData:
    def __init__(self, items: dict[str, Any], fields: dict[str, Any]):
        self.items = items
        self.fields = fields
