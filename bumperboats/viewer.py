import math
from ipycanvas import Canvas


class CanvasViewer:
    def __init__(self, engine, sensor, canvas):
        self.engine = engine
        self.sensor = sensor
        self.canvas = canvas
        self.canvas.stroke_style = 'black'
        self.canvas.stroke_rect(0,0, self.canvas.width, self.canvas.height)

    def tick(self):
        self.canvas.stroke_style = 'blue'
        for boat, _ in self.engine.boats:
            self.canvas.stroke_arc(boat.position[0], boat.position[1], boat.radius, 0, 2 * math.pi)

        self.canvas.stroke_style = 'red'
        for contact in self.sensor.contacts:
            self.canvas.stroke_arc(contact[0], contact[1], 1, 0, 2 * math.pi)

