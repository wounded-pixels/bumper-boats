from collections import namedtuple

Snapshot = namedtuple('Snapshot', 'state estimated_position measurement residual mahalanobis log_likelihood actual_position actual_state actual_id elapsed covariance')
