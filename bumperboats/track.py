import numpy as np
from scipy.linalg import block_diag

from filterpy.kalman import KalmanFilter
import filterpy.common


class SimpleFirstOrderKFTrack:
    def __init__(self, dt, std):
        self.kf = KalmanFilter(dim_x=4, dim_z=2)

        # state transition function
        self.kf.F = np.array([
            [1, dt, 0, 0],
            [0,  1, 0, 0],
            [0,  0, 1, dt],
            [0,  0, 0, 1],
        ])

        # Process noise
        q = filterpy.common.Q_discrete_white_noise(dim=2, dt=dt, var=0.1)
        self.kf.Q = block_diag(q, q)

        # measurement matrix state -> measurement space
        self.kf.H = np.array([
            [1, 0, 0, 0],
            [0, 0, 1, 0]
        ])

        # initial state
        self.kf.x = np.array([[0, 0, 0, 0]]).T

        # initial covariance matrix - weak flat prior
        self.kf.P = np.eye(4) * 500.

        # Measurement noise
        self.kf.R = np.eye(2).dot(std*std)

    def on_data(self, z_measurement):
        self.kf.predict()
        self.kf.update(z_measurement)

    def get_position_estimate(self):
        return self.kf.H.dot(self.kf.x)

    def print_diagnostics(self):
        print('kf\n', self.kf)


class SimpleSecondOrderKFTrack:
    def __init__(self, dt, std):
        self.kf = KalmanFilter(dim_x=6, dim_z=2)

        # state transition function
        self.kf.F = np.array([
            [1, dt, 0.5*dt*dt, 0, 0, 0],
            [0,  1, dt,        0, 0, 0],
            [0,  0, 1,         0, 0, 0],
            [0,  0, 0,         1, dt, 0.5*dt*dt],
            [0,  0, 0,         0, 1,  dt],
            [0,  0, 0,         0,  0, 1],
        ])

        # Process noise
        q = filterpy.common.Q_discrete_white_noise(dim=3, dt=dt, var=0.1)
        self.kf.Q = block_diag(q, q)

        # measurement matrix state -> measurement space
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0]
        ])

        # initial state
        self.kf.x = np.array([[0, 0, 0, 0, 0, 0]]).T

        # initial covariance matrix - weak flat prior
        self.kf.P = np.eye(6) * 500.

        # Measurement noise
        self.kf.R = np.eye(2).dot(std*std)

    def on_data(self, z_measurement):
        self.kf.predict()
        self.kf.update(z_measurement)

    def get_position_estimate(self):
        return self.kf.H.dot(self.kf.x)

    def print_diagnostics(self):
        print('kf\n', self.kf)
