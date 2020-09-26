import numpy as np

from bumperboats.associators import SimpleAssociator
from bumperboats.boat import Boat
from bumperboats.controllers import FixedController, OscillatingController
from bumperboats.physics import SimpleEngine
from bumperboats.sensors import SimplePositionSensor
from bumperboats.viewer import PlotViewer

dt = 0.5
measurement_std = 1
max_steps = round(100/dt)

associator = SimpleAssociator(std=measurement_std * 1.1, max_velocity=12., max_acceleration=12., max_bearing_change=70)
engine = SimpleEngine()
sensor = SimplePositionSensor(engine, std=measurement_std, period=0.5, min_value=-200)
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

overall_nees = []
for track in associator.get_tracks():
    NEES_list = track.calculate_NEES_list()
    overall_NEES = [*overall_nees, *NEES_list]
    print('ids', track.actual_ids(), 'mean_nees', np.mean(NEES_list))

print('overall mean NEES', np.mean(overall_NEES))

