import numpy as np

from bumperboats.associators import FakeAssociator
from bumperboats.boat import Boat
from bumperboats.controller import FixedController
from bumperboats.physics import SimpleEngine
from bumperboats.sensors import SimplePositionSensor
from bumperboats.viewer import PlotViewer

associator = FakeAssociator()
engine = SimpleEngine()
sensor = SimplePositionSensor(engine, std=3, period=1)
sensor.add_destination(associator)
viewer = PlotViewer(engine, sensor, associator)

circle_boat = Boat(np.array([325., 325.]), 0., np.array([0., 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=1.25, thrust_angle=30.)
engine.add_boat(circle_boat, controller)

straight_boat = Boat(np.array([100., 200.]), 0., np.array([0., 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=0.25, thrust_angle=0.)
engine.add_boat(straight_boat, controller)

dt = 0.5
for _ in range(240):
    engine.tick(dt)
    sensor.tick(dt)
    viewer.tick()

viewer.show()
associator.print_diagnostics()
