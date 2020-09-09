from matplotlib.pyplot import plot
from matplotlib import pyplot as plt


class PlotViewer:
    def __init__(self, engine, sensor, track):
        self.engine = engine
        self.sensor = sensor
        self.track = track

    def tick(self):
        for boat, _ in self.engine.boats:
            plot(boat.position[0], boat.position[1], '.', c='blue')

        for contact in self.sensor.contacts:
            plot(contact[0], contact[1], '.', c='red')

        x = self.track.get_position_estimate()
        plot(x[0], x[1], '.', c='green')

    @staticmethod
    def show():
        plt.show()
