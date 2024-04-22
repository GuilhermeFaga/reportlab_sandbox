from reportlab.platypus import Flowable

from svglib.svglib import svg2rlg


class Icon(Flowable):

    def __init__(
        self, svg_path: str, width: int = 0, height: int = 0, debug_flag: int = 0
    ):
        self.svg_path = svg_path
        self.width = width
        self.height = height
        self.debug_flag = debug_flag

        self.icon = svg2rlg(self.svg_path)

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        if not self.icon:
            return (self.max_width, self.max_height)

        if self.width:
            self.resizeWidth(self.width)
        if self.height:
            self.resizeHeight(self.height)

        return (self.icon.width, self.icon.height)

    def draw(self):
        if not self.icon:
            return

        self.canv.saveState()

        if self.width:
            self.resizeWidth(self.width)
        if self.height:
            self.resizeHeight(self.height)

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
