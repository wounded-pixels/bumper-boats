import numpy as np

from bumperboats.associators import SimpleAssociator, FakeAssociator
from bumperboats.boat import Boat
from bumperboats.controllers import FixedController, OscillatingController
from bumperboats.physics import SimpleEngine
from bumperboats.sensors import SimplePositionSensor
from bumperboats.viewer import PlotViewer

dt = 0.5
max_steps = round(100/dt)

fake_associator = FakeAssociator()
associator = SimpleAssociator(max_velocity=15., max_acceleration=8., max_bearing_change=70)
engine = SimpleEngine()
sensor = SimplePositionSensor(engine, std=3, period=2, min_value=-200)
sensor.add_destination(associator)
viewer = PlotViewer(engine, sensor, associator)

boat = Boat(np.array([325., 325.]), 0., np.array([0., 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=0.5, thrust_angle=30.)
engine.add_boat(boat, controller)

boat = Boat(np.array([50., 125.]), 0., np.array([0.5, 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=0.5, thrust_angle=0.)
engine.add_boat(boat, controller)

boat = Boat(np.array([50., 215.]), 0., np.array([0.5, 0.]), np.array([0.5, 0.]))
controller = OscillatingController(thrust=0.5, thrust_angle=-15.)
engine.add_boat(boat, controller)

for ctr in range(max_steps):
    engine.tick(dt)
    sensor.tick(dt)
    if ctr > 0 and ctr % 20 == 0 or ctr == max_steps-1:
        associator.prune()
        viewer.show(title='ctr: '+str(ctr))

