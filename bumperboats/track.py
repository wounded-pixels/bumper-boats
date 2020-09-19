import numpy as np
from scipy.linalg import block_diag

from filterpy.kalman import KalmanFilter
import filterpy.common

from bumperboats.snapshot import Snapshot


class SimpleSecondOrderKFTrack:
    def __init__(self, contact, dt, std):
        self.contact = contact
        self.snapshots = []

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
        q = filterpy.common.Q_discrete_white_noise(dim=3, dt=dt, var=1.5)
        self.kf.Q = block_diag(q, q)

        # measurement matrix state -> measurement space
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0]
        ])

        # initial state
        self.kf.x = np.array([[contact.measurement[0], 0, 0, contact.measurement[1], 0, 0]]).T

        # initial covariance matrix - weak flat prior
        self.kf.P = np.eye(6) * 500.

        # Measurement noise
        self.kf.R = np.eye(2).dot(std*std)

        self.snapshots.append(Snapshot(state=self.kf.x,
                                       estimate=self.kf.H.dot(self.kf.x),
                                       measurement=self.contact.measurement,
                                       residual=self.kf.y,
                                       mahalanobis=self.kf.mahalanobis,
                                       log_likelihood=self.kf.log_likelihood,
                                       actual=self.contact.actual,
                                       actual_id=self.contact.actual_id)
                              )

    def predict(self):
        self.kf.predict()

    def on_data(self, contact):
        self.contact = contact
        self.kf.update(contact.measurement)
        self.snapshots.append(Snapshot(state=self.kf.x,
                                       estimate=self.kf.H.dot(self.kf.x),
                                       measurement=self.contact.measurement,
                                       residual=self.kf.y,
                                       mahalanobis=self.kf.mahalanobis,
                                       log_likelihood=self.kf.log_likelihood,
                                       actual=self.contact.actual,
                                       actual_id=self.contact.actual_id)
                              )

    def get_snapshots(self):
        return self.snapshots

    def print_diagnostics(self):
        print('kf\n', self.kf.log_likelihood)

    def actual_ids(self):
        return ','.join([str(snapshot.actual_id) for snapshot in self.snapshots])

    def velocity(self):
        return np.array([self.kf.x[1], self.kf.x[4]])

    def velocity_norm(self):
        return np.linalg.norm(self.velocity())

    def acceleration(self):
        return np.array([self.kf.x[2], self.kf.x[5]])

    def acceleration_norm(self):
        return np.linalg.norm(self.acceleration())
