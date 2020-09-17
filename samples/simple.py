import numpy as np

from bumperboats.associators import SimpleAssociator
from bumperboats.boat import Boat
from bumperboats.controllers import FixedController, OscillatingController
from bumperboats.physics import SimpleEngine
from bumperboats.sensors import SimplePositionSensor
from bumperboats.viewer import PlotViewer

dt = 0.5
associator = SimpleAssociator()
engine = SimpleEngine()
sensor = SimplePositionSensor(engine, std=3, period=1)
sensor.add_destination(associator)
viewer = PlotViewer(engine, sensor, associator)

boat = Boat(np.array([325., 325.]), 0., np.array([0., 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=1.25, thrust_angle=30.)
engine.add_boat(boat, controller)

boat = Boat(np.array([50., 125.]), 0., np.array([0.5, 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=0.25, thrust_angle=0.)
engine.add_boat(boat, controller)

boat = Boat(np.array([50., 175.]), 0., np.array([0.5, 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=0.25, thrust_angle=0.)
engine.add_boat(boat, controller)

boat = Boat(np.array([50., 215.]), 0., np.array([0.5, 0.]), np.array([0.5, 0.]))
controller = OscillatingController(thrust=0.3, thrust_angle=-15.)
engine.add_boat(boat, controller)

for ctr in range(300):
    engine.tick(dt)
    sensor.tick(dt)
    if ctr > 0 and ctr % 25 == 0:
        viewer.show()
        associator.print_diagnostics()
