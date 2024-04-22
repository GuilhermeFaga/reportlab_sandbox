from reportlab.platypus import Flowable

from svglib.svglib import svg2rlg


class Icon(Flowable):

    def __init__(self, svg_path: str, width: int = 0, height: int = 0):
        self.svg_path = svg_path
        self.width = width
        self.height = height

        self.icon = svg2rlg(self.svg_path)

    def wrap(self, aW, aH):
        self.max_width = aW
        self.max_height = aH

        return (self.max_width, self.max_height)

    def draw(self):
        if not self.icon:
            return

        self.canv.saveState()

        self.icon.width = self.width
        self.icon.height = self.height

        self.icon.drawOn(self.canv, 0, 0)

        self.canv.restoreState()
