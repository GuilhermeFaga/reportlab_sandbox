from src.enums import Colors


class IconCardData:
    def __init__(self, title: str, description: str, icon, color: Colors = Colors.Gray):
        self.title = title
        self.description = description
        self.icon = icon
        self.color = color
