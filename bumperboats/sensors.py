import numpy as np

from bumperboats.contact import Contact


class SimplePositionSensor:
    def __init__(self, engine, std, period, min_value=0, max_value=600):
        self.engine = engine
        self.std = std
        self.period = period
        self.min_value = min_value
        self.max_value = max_value
        self.destinations = []
        self.elapsed = 0
        self.since = 0
        self.contacts = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def noise(self):
        return np.array(np.random.normal(0, self.std, 2))

    def tick(self, dt):
        self.elapsed += dt
        self.since += dt
        if self.since >= self.period:
            self.contacts = [
                Contact(measurement=np.array([boat.position[0], boat.position[1]]) + self.noise(),
                        actual_position=np.array([boat.position[0], boat.position[1]]),
                        actual_state=np.array([boat.position[0], boat.velocity[0], boat.acceleration[0],boat.position[1], boat.velocity[1], boat.acceleration[1]]),
                        actual_id=boat.id,
                        elapsed=self.elapsed)
                for boat, controller in self.engine.boats
                if self.min_value < boat.position[0] < self.max_value and
                   self.min_value < boat.position[1] < self.max_value
            ]

            for destination in self.destinations:
                destination.on_data(contacts=self.contacts, dt=self.since)

            self.since = 0
