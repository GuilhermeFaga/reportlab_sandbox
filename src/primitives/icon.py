from reportlab.platypus import Flowable

from reportlab.graphics.shapes import Path

from svglib.svglib import svg2rlg

from src.enums import Colors, SvgPath


class Icon(Flowable):

    def __init__(
        self,
        svg_path: SvgPath,
        width: int = 0,
        height: int = 0,
        color: Colors = Colors.Black,
        opacity=1,
        debug_flag: int = 0,
    ):
        self.svg_path = svg_path
        self.iWidth = width
        self.iHeight = height
        self.color = color
        self.opacity = opacity
        self.debug_flag = debug_flag

        self.icon = svg2rlg(self.svg_path.value)

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        if not self.icon:
            return (self.max_width, self.max_height)

        if self.iWidth:
            self.resizeWidth(self.iWidth)
        if self.iHeight:
            self.resizeHeight(self.iHeight)

        self.width = self.icon.width
        self.height = self.icon.height

        return (self.icon.width, self.icon.height)

    def draw(self):
        if not self.icon:
            return

        self.canv.saveState()

        self.changeColor(self.color)
        self.changeOpacity(self.opacity)

        self.icon._showBoundary = self.debug_flag  # type: ignore

        self.icon.drawOn(self.canv, 0, 0)

        self.canv.restoreState()

    def resizeWidth(self, width: int):
        if not self.icon:
            return
        scaling_factor = width / self.icon.width
        self.icon.width = width
        self.icon.height = int(self.icon.height * scaling_factor)
        self.icon.scale(scaling_factor, scaling_factor)

    def resizeHeight(self, height: int):
        if not self.icon:
            return
        scaling_factor = height / self.icon.height
        self.icon.width = int(self.icon.width * scaling_factor)
        self.icon.height = height
        self.icon.scale(scaling_factor, scaling_factor)

    def getShapes(self) -> list[Path]:
        if not self.icon:
            return []

        shapes: list[Path] = []

        next = self.icon
        while next:
            if isinstance(next, Path):
                shapes.append(next)

            if hasattr(next, "contents"):
                next = next.getProperties().get("contents", [])[0]
            else:
                next = None

        return shapes

    def changeColor(self, color: Colors):
        if not self.icon:
            return

        children: list[Path] = self.getShapes()

        for shape in children:
            if hasattr(shape, "fillColor"):
                shape.setProperties({"fillColor": Colors.getIconColor(color).value})

    def changeOpacity(self, opacity: float):
        if not self.icon:
            return

        children: list[Path] = self.getShapes()

        for shape in children:
            if hasattr(shape, "fillOpacity"):
                shape.setProperties({"fillOpacity": opacity})
