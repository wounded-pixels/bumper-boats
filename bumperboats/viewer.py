from matplotlib import pyplot as plt


class PlotViewer:
    def __init__(self, engine, sensor, associator):
        self.engine = engine
        self.sensor = sensor
        self.associator = associator

        self.fig, (self.position_ax, self.residual_ax) = plt.subplots(2, 1, figsize=(12, 12))

    def show(self):
        for track in self.associator.get_tracks():
            xs = []
            ys = []
            mxs = []
            mys = []
            exs = []
            eys = []
            mr_xs = []
            mr_ys = []
            er_xs = []
            er_ys = []
            for snapshot in track.get_snapshots():
                xs.append(snapshot.actual[0])
                ys.append(snapshot.actual[1])

                mxs.append(snapshot.measurement[0])
                mys.append(snapshot.measurement[1])
                mr_xs.append(snapshot.measurement[0] - snapshot.actual[0])
                mr_ys.append(snapshot.measurement[1] - snapshot.actual[1])

                exs.append(snapshot.estimate[0])
                eys.append(snapshot.estimate[1])
                er_xs.append(snapshot.estimate[0] - snapshot.actual[0])
                er_ys.append(snapshot.estimate[1] - snapshot.actual[1])

            self.position_ax.plot(xs, ys, c='blue')
            self.position_ax.plot(mxs, mys, '.', c='red')
            self.position_ax.plot(exs, eys, '.', c='green')

            self.residual_ax.plot(mr_xs, mr_ys, '.', c='red')
            self.residual_ax.plot(er_xs, er_ys, '.', c='green')

        radius = 8
        self.residual_ax.hlines([0], xmin=-radius, xmax=radius)
        self.residual_ax.vlines([0], ymin=-radius, ymax=radius)
        plt.show()

        self.fig, (self.position_ax, self.residual_ax) = plt.subplots(2, 1, figsize=(12, 12))
