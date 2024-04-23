from enum import Enum
from typing import Final


class Colors(Enum):
    Black: Final = "#000000"
    Black_70: Final = "#4D4D4D"
    White: Final = "#FFFFFF"
    Gray: Final = "#E6E6E6"
    DarkGray: Final = "#B3B3B3"
    Red: Final = "#E13655"
    Orange: Final = "#F1975F"
    Green: Final = "#9BB460"
    Blue: Final = "#479AAE"

    DarkOrange: Final = "#794C30"
    DarkGreen: Final = "#4E5A30"

    @staticmethod
    def getTextColor(color: "Colors"):
        if color == Colors.Black:
            return Colors.White
        if color == Colors.White:
            return Colors.Black
        if color == Colors.Red:
            return Colors.White
        if color == Colors.Orange:
            return Colors.Black
        if color == Colors.Green:
            return Colors.Black
        return Colors.Black

    @staticmethod
    def getIconColor(color: "Colors"):
        if color == Colors.Black:
            return Colors.White
        if color == Colors.Red:
            return Colors.White
        if color == Colors.Orange:
            return Colors.DarkOrange
        if color == Colors.Green:
            return Colors.DarkGreen
        return color
