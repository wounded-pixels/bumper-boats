import numpy as np
from copy import deepcopy

from bumperboats import track
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
        if self.prune_ctr > 5:
            self.prune_ctr = 0
            self.prune()

        old_tracks = self.tracks

        self.tracks = []

        for track in old_tracks:
            track.predict()

        for contact in contacts:
            match = False
            print('contact tracks ', len(old_tracks))
            for track in deepcopy(old_tracks):
                track.on_data(contact)
                distance = np.linalg.norm(track.kf.y)
                if track.kf.mahalanobis < 3:
                    self.tracks.append(track)
                    print('Accept mahalanois', track.kf.mahalanobis, 'distance ', distance)
                    match = True
                else:
                    print('reject mahalanois', track.kf.mahalanobis, 'distance ', distance)

            if not match:
                self.tracks.append(SimpleSecondOrderKFTrack(contact, dt=1, std=3))

    def get_tracks(self):
        return self.tracks

    def prune(self):
        old_tracks = self.tracks
        self.tracks = [track for track in old_tracks if track.kf.log_likelihood > -10]

    def print_diagnostics(self):
        print('track count', len(self.tracks))
        for track in self.tracks:
            track.print_diagnostics()
