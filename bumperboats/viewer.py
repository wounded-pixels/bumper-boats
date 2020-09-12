import math
from matplotlib import pyplot as plt


class PlotViewer:
    def __init__(self, engine, sensor, associator):
        self.engine = engine
        self.sensor = sensor
        self.associator = associator

        self.values_x_map = {}
        self.values_y_map = {}

        self.measurements_x_map = {}
        self.measurements_y_map = {}

        self.estimates_x_map = {}
        self.estimates_y_map = {}

        self.measurement_residuals_map = {}
        self.estimate_residuals_map = {}

        self.fig, (self.position_ax, self.residual_ax) = plt.subplots(2, 1, figsize=(12, 12))

    def tick(self):
        for boat, _ in self.engine.boats:
            positions_x = self.values_x_map.setdefault(boat.id, [])
            positions_y = self.values_y_map.setdefault(boat.id, [])
            positions_x.append(boat.position[0])
            positions_y.append(boat.position[1])

        for contact, actual_id in self.sensor.contacts:
            measurements_x = self.measurements_x_map.setdefault(actual_id, [])
            measurements_y = self.measurements_y_map.setdefault(actual_id, [])
            measurements_x.append(contact[0])
            measurements_y.append(contact[1])

        for track_id, track in self.associator.track_map.items():
            pe = track.get_position_estimate()

            estimates_x = self.estimates_x_map.setdefault(track_id, [])
            estimates_y = self.estimates_y_map.setdefault(track_id, [])
            estimates_x.append(pe[0])
            estimates_y.append(pe[1])

    def show(self):
        for value_id in self.values_x_map.keys():
            xs = self.values_x_map[value_id]
            ys = self.values_y_map[value_id]
            mxs = self.measurements_x_map[value_id]
            mys = self.measurements_y_map[value_id]
            exs = self.estimates_x_map[value_id]
            eys = self.estimates_y_map[value_id]

            measurement_residuals_xs = [mx-x for mx, x in zip(mxs, xs)]
            measurement_residuals_ys = [my-y for my, y in zip(mys, ys)]
            estimation_residuals_xs = [ex-x for ex, x in zip(exs, xs)]
            estimation_residuals_ys = [ey-y for ey, y in zip(eys, ys)]

            self.position_ax.plot(xs, ys, c='blue')
            self.position_ax.plot(mxs, mys, '.', c='red')
            self.position_ax.plot(exs, eys, '.', c='green')

            self.residual_ax.plot(measurement_residuals_xs, measurement_residuals_ys, '.', c='red')
            self.residual_ax.plot(estimation_residuals_xs, estimation_residuals_ys, '.', c='green')

        radius = 8
        self.residual_ax.hlines([0], xmin=-radius, xmax=radius)
        self.residual_ax.vlines([0], ymin=-radius, ymax=radius)
        plt.show()
