import math
from ipycanvas import Canvas


class CanvasViewer:
    def __init__(self, engine, canvas):
        self.engine = engine
        self.canvas = canvas
        self.canvas.stroke_style = 'black'
        self.canvas.stroke_rect(0,0, self.canvas.width, self.canvas.height)
        self.canvas.stroke_style = 'blue'

    def tick(self):
        for boat, _ in self.engine.boats:
            self.canvas.stroke_arc(boat.position[0], boat.position[1], boat.radius, 0, 2 * math.pi)

