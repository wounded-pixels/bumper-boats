import math

import numpy as np


def vector_norm(vec):
    return np.linalg.norm(vec, ord=1)


class SimpleEngine:
    def __init__(self, resistance_coefficient=0.0314):
        self.resistance_coefficient = resistance_coefficient
        self.boats = []

    def __repr__(self):
        return '\n'.join([str(boat) for boat in self.boats])

    def tick(self, dt):
        for boat, controller in self.boats:
            speed = vector_norm(boat.velocity)

            resistance_acceleration = np.array([0, 0])
            if speed > 0.0001:
                direction = boat.velocity / speed
                resistance_magnitude = -1 * math.pi * boat.radius * speed * self.resistance_coefficient
                resistance_acceleration = resistance_magnitude * direction

            thrust_acceleration = controller.calculate_thrust_acceleration(boat)
            boat.acceleration = thrust_acceleration + resistance_acceleration
            boat.tick(dt)

    def add_boat(self, boat, controller):
        self.boats.append((boat, controller))
