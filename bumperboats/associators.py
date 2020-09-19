import numpy as np
from copy import deepcopy

from bumperboats.track import SimpleSecondOrderKFTrack


class FakeAssociator:
    def __init__(self):
        self.track_map = {}

    def on_data(self, contacts):
        for track in self.get_tracks():
            track.predict()

        for contact in contacts:
            track = self.track_map.setdefault(contact.actual_id, SimpleSecondOrderKFTrack(contact, dt=1, std=3))
            track.on_data(contact)

    def get_tracks(self):
        return [track for _, track in self.track_map.items()]

    def print_diagnostics(self):
        for track in self.get_tracks():
            track.print_diagnostics()


class SimpleAssociator:
    def __init__(self, max_velocity, max_acceleration):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.tracks = []
        self.prune_ctr = 0

    def print_track_actuals(self, spot):
        tas = [t.actual_ids()+' '+str(t.velocity_norm())+' '+str(t.acceleration_norm()) for t in self.tracks]
        if tas:
            print(spot)
            print('\n'.join(sorted(tas)))

    def on_data(self, contacts):
        self.prune_ctr += 1
        if self.prune_ctr > 3:
            self.prune_ctr = 0
            self.prune()

        old_tracks = self.tracks
        self.tracks = []

        for old_track in old_tracks:
            old_track.predict()

        for contact in contacts:
            matches = []
            best_residual_norm = 10000
            for track in deepcopy(old_tracks):
                track.on_data(contact)
                if track.velocity_norm() < self.max_velocity and track.acceleration_norm() < self.max_acceleration:
                    matches.append(track)
                    residual_norm = np.linalg.norm(track.kf.y)
                    best_residual_norm = min(best_residual_norm, residual_norm)
                else:
                    print('rejecting velocity', track.velocity_norm(), 'vs', self.max_velocity, 'acceleration', track.acceleration_norm(), 'vs', self.max_acceleration, 'ids', track.actual_ids())

            if len(matches) > 0 and best_residual_norm < 20000:
                for match in matches:
                    if np.linalg.norm(match.kf.y) < best_residual_norm * 13:
                        self.tracks.append(match)
            else:
                self.tracks.append(SimpleSecondOrderKFTrack(contact, dt=1, std=3))

        print('\n----------')
        print('len(contacts)', len(contacts), 'len(self.tracks)', len(self.tracks))
        #self.print_track_actuals('onData')

    def get_tracks(self):
        return self.tracks

    def prune(self):
        old_tracks = self.tracks
        self.tracks = []

        for old_track in old_tracks:
            keep = True
            for snapshot in old_track.snapshots:
                if snapshot.mahalanobis > 3:
                    keep = False
                    print('knock out mahalanobis ', snapshot.mahalanobis)

            bad_count = 0
            for index, snapshot in enumerate(old_track.snapshots):
                if index > 1 and snapshot.log_likelihood < -10:
                    bad_count += 1

            bad_count_ratio = bad_count/len(old_track.snapshots)
            if len(old_track.snapshots) > 8 and bad_count_ratio > 0.05:
                print('knockout bad_count_ratio', bad_count_ratio, old_track.actual_ids())
                keep = False

            if keep:
                self.tracks.append(old_track)

        self.print_track_actuals('prune')
