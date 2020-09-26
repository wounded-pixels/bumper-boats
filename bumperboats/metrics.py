import numpy as np
from scipy.linalg import inv


def NEES(snapshot):
    err = snapshot.actual_state - snapshot.state.flatten()
    return np.dot(err.T, inv(snapshot.covariance)).dot(err)
