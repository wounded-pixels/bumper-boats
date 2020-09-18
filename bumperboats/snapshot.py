from collections import namedtuple

Snapshot = namedtuple('Snapshot', 'state estimate measurement residual mahalanobis log_likelihood actual actual_id')
