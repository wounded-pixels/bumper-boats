import numpy as np
from scipy.linalg import block_diag

from filterpy.kalman import KalmanFilter
import filterpy.common

from bumperboats.physics import vector_norm, degrees_between
from bumperboats.snapshot import Snapshot


class SimpleSecondOrderKFTrack:
    def __init__(self, contact, dt, std, max_velocity, max_acceleration, max_bearing_change):
        self.contact = contact
        self.dt = dt
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.max_bearing_change = max_bearing_change

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

    def actually_consistent(self):
        ids = [snapshot.actual_id for snapshot in self.snapshots]
        return np.amin(ids) == np.amax(ids)

    def position(self):
        return self.snapshots[-1].estimate.T[0]

    def prior_position(self):
        return self.snapshots[-2].estimate.T[0]

    def prior_prior_position(self):
        return self.snapshots[-3].estimate.T[0]

    def velocity(self):
        if len(self.snapshots) > 1:
            return (self.position() - self.prior_position()) / (self.dt * 2)
        else:
            return np.array([0.,0.])

    def prior_velocity(self):
        if len(self.snapshots) > 2:
            return (self.prior_position() - self.prior_prior_position()) / (self.dt * 2)
        else:
            return np.array([0.,0.])

    def velocity_norm(self):
        return vector_norm(self.velocity())

    def acceleration(self):
        return np.array([self.kf.x[2][0], self.kf.x[5][0]])

    def acceleration_norm(self):
        return vector_norm(self.acceleration())

    def bearing_change(self):
        return degrees_between(self.velocity(), self.prior_velocity())

    def is_maneuver_possible(self):
        if self.velocity_norm() > self.max_velocity:
            if self.actually_consistent():
                print('rejecting velocity', self.velocity_norm(), '>', self.max_velocity, self.actual_ids())
            return False

        if self.acceleration_norm() > self.max_acceleration:
            if self.actually_consistent():
                print('rejecting acceleration', self.acceleration_norm(), '>', self.max_acceleration, self.actual_ids())
            return False

        if abs(self.bearing_change()) > self.max_bearing_change:
            if self.actually_consistent():
                print('rejecting bearing', self.bearing_change(), '>', self.max_bearing_change, 'position', self.position(), 'prior_position', self.prior_position(), 'velocity', self.velocity(), 'prior_velocity', self.prior_velocity(), self.actual_ids())
            return False

        return True