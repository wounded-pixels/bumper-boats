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
    def __init__(self):
        self.tracks = []
        self.prune_ctr = 0

    def on_data(self, contacts):
        self.prune_ctr += 1
        if self.prune_ctr > 1:
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
                residual_norm = np.linalg.norm(track.kf.y)
                matches.append(track)
                best_residual_norm = min(best_residual_norm, residual_norm)

            if len(matches) > 0 and best_residual_norm < 200:
                for match in matches:
                    if np.linalg.norm(match.kf.y) < best_residual_norm * 2.0:
                        self.tracks.append(match)
            else:
                self.tracks.append(SimpleSecondOrderKFTrack(contact, dt=1, std=3))

        print('len(contacts', len(contacts), 'len(self.tracks)', len(self.tracks))

    def get_tracks(self):
        return self.tracks

    def prune(self):
        old_tracks = self.tracks
        self.tracks = []

        for old_track in old_tracks:
            keep = True
            for snapshot in old_track.snapshots:
                if snapshot.mahalanobis > 10:
                    keep = False
                    print('knock out mahalanobis ', snapshot.mahalanobis)

            bad_count = 0
            for index, snapshot in enumerate(old_track.snapshots):
                if index > 1 and snapshot.log_likelihood < -10:
                    bad_count += 1

            bad_count_ratio = bad_count/len(old_track.snapshots)
            if len(old_track.snapshots) > 8 and bad_count_ratio > 0.05:
                print('knockout bad_count_ratio', bad_count_ratio)
                keep = False

            if keep:
                self.tracks.append(old_track)

    def print_diagnostics(self):
        print('track count', len(self.tracks))
        for track in self.tracks:
            track.print_diagnostics()
