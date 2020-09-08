import math

class Boat:
    def __init__(self, position, heading, velocity, acceleration, radius = 1):
        self.position = position
        self.heading = heading
        self.velocity = velocity
        self.acceleration = acceleration
        self.radius = radius

    def __repr__(self):
        return 'Boat(position=%r, heading=%r, velocity=%r, acceleration=%r, radius=%r)' % (self.position, self.heading, self.velocity, self.acceleration, self.radius)

    def tick(self, dt):
        self.position = self.position + self.velocity * dt + 0.5 * dt * dt * self.acceleration
        self.velocity = self.velocity + self.acceleration * dt
        if abs(self.velocity[0]) > 0.0000000001:
            self.heading = math.atan(self.velocity[1] / self.velocity[0]) * (180 / math.pi)

