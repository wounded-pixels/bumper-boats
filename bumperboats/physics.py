import math

import numpy as np


def vector_norm(vector):
    return np.linalg.norm(vector, ord=1)


def unit_vector(vector):
    return vector / vector_norm(vector)


def degrees_between(vector1, vector2):
    if np.isclose(vector1, vector2).all():
        return 0

    unit_vector1 = unit_vector(vector1)
    unit_vector2 = unit_vector(vector2)
    cos_angle = np.dot(unit_vector1, unit_vector2)
    radians = np.arccos(cos_angle)
    return np.rad2deg(radians)


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
