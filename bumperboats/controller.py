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
