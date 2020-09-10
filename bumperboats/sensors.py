import numpy as np


class SimplePositionSensor:
    def __init__(self, engine, std, period):
        self.engine = engine
        self.std = std
        self.period = period
        self.destinations = []
        self.elapsed = 0
        self.contacts = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def noise(self):
        return np.array(np.random.normal(0, self.std, 2))

    def tick(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.period:
            self.elapsed = 0
            self.contacts = [(np.array([boat.position[0], boat.position[1]]) + self.noise(), boat.id) for boat, controller in
                             self.engine.boats]
            for destination in self.destinations:
                destination.on_data(self.contacts)
