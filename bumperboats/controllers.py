import math
import numpy as np


class FixedController:
    def __init__(self, thrust, thrust_angle):
        self.thrust = thrust
        self.thrust_angle = thrust_angle

    def calculate_thrust_acceleration(self, boat):
        thrust_radians = (boat.heading + self.thrust_angle) * (math.pi / 180)
        thrust_direction = np.array([math.cos(thrust_radians), math.sin(thrust_radians)])
        return self.thrust * thrust_direction


class OscillatingController:
    def __init__(self, thrust, thrust_angle):
        self.thrust = thrust
        self.max_thrust_angle = abs(thrust_angle)
        self.thrust_angle = thrust_angle
        self.increment = -1

    def calculate_thrust_acceleration(self, boat):
        self.thrust_angle += self.increment

        if abs(self.thrust_angle) > self.max_thrust_angle:
            self.increment *= -1

        thrust_radians = (boat.heading + self.thrust_angle) * (math.pi / 180)
        thrust_direction = np.array([math.cos(thrust_radians), math.sin(thrust_radians)])
        return self.thrust * thrust_direction
