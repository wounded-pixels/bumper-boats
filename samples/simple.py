import numpy as np

from bumperboats.boat import Boat
from bumperboats.controller import FixedController
from bumperboats.physics import SimpleEngine
from bumperboats.sensors import SimpleSensor
from bumperboats.track import SimplePositionKFTrack
from bumperboats.viewer import PlotViewer

track = SimplePositionKFTrack(dt=1, std=3)
engine = SimpleEngine()
sensor = SimpleSensor(engine, std=3, period=1)
sensor.add_destination(track)
viewer = PlotViewer(engine, sensor, track)

boat = Boat(np.array([325., 325.]), 0., np.array([0., 0.]), np.array([0.5, 0.]))
controller = FixedController(thrust=1.25, thrust_angle=30.)
engine.add_boat(boat, controller)


dt = 0.5
for _ in range(240):
    engine.tick(dt)
    sensor.tick(dt)
    viewer.tick()

viewer.show()
track.print_diagnostics()
