from copy import deepcopy

from bumperboats.track import SimpleSecondOrderKFTrack


class FakeAssociator:
    def __init__(self):
        self.track_map = {}

    def on_data(self, contacts):
        for track in self.get_tracks():
            track.predict()

        for contact in contacts:
            track = self.track_map.setdefault(contact.actual_id,
                                              SimpleSecondOrderKFTrack(contact, dt=1, std=3,
                                                                       max_velocity=100,
                                                                       max_acceleration=100,
                                                                       max_bearing_change=100))
            track.on_data(contact)

    def get_tracks(self):
        return [track for _, track in self.track_map.items()]

    def print_diagnostics(self):
        for track in self.get_tracks():
            track.print_diagnostics()


class SimpleAssociator:
    def __init__(self, max_velocity, max_acceleration,max_bearing_change):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.max_bearing_change = max_bearing_change
        self.tracks = []
        self.dead_tracks = []
        self.prune_ctr = 0
        self.tick_ctr = 0

    def print_track_actuals(self, spot):
        print(spot)
        for t in self.get_tracks():
            if t.actually_consistent():
                print('All', t.snapshots[-1].actual_id, 'x', len(t.snapshots), 'velocity_norm', t.velocity_norm(),
                      'acceleration_norm', t.acceleration_norm(), 'bearing change', t.bearing_change())

        for t in self.get_tracks():
            if not t.actually_consistent():
                print(t.actual_ids(), 'velocity_norm', t.velocity_norm(), 'bearing change',
                      t.bearing_change(), 'acceleration_norm', t.acceleration_norm())

    def on_data(self, contacts):
        self.tick_ctr += 1
        self.prune_ctr += 1
        if self.prune_ctr > 3:
            self.prune_ctr = 0
            self.prune()

        dead_track_ids = [track.id for track in self.tracks]
        old_tracks = self.tracks
        self.tracks = []

        for old_track in old_tracks:
            old_track.predict()

        for contact in contacts:
            matched = False
            for track in deepcopy(old_tracks):
                track.on_data(contact)
                if track.is_maneuver_possible():
                    self.tracks.append(track)
                    matched = True
                    if track.id in dead_track_ids:
                        dead_track_ids.remove(track.id)

            if not matched:
                self.tracks.append(SimpleSecondOrderKFTrack(contact, dt=1, std=5, max_velocity=self.max_velocity, max_acceleration=self.max_acceleration, max_bearing_change=self.max_bearing_change))

        # inefficient but n should be small...
        for dead_track_id in dead_track_ids:
            for track in deepcopy(old_tracks):
                if track.id == dead_track_id:
                    self.dead_tracks.append(track)

        print('\n----------')
        print('tick', self.tick_ctr, 'len(contacts)', len(contacts), 'len(self.tracks)', len(self.tracks))
        self.print_track_actuals('onData')

    def get_tracks(self):
        return [*self.tracks, *self.dead_tracks]

    def prune(self):
        old_tracks = self.tracks
        self.tracks = []

        for old_track in old_tracks:
            keep = True
            for snapshot in old_track.snapshots:
                if snapshot.mahalanobis > 3:
                    keep = False
                    if old_track.actually_consistent():
                        print('prune rejecting mahalanobis ', snapshot.mahalanobis, old_track.actual_ids)

            bad_count = 0
            for index, snapshot in enumerate(old_track.snapshots):
                if index > 1 and snapshot.log_likelihood < -10:
                    bad_count += 1

            bad_count_ratio = bad_count/len(old_track.snapshots)
            if len(old_track.snapshots) > 8 and bad_count_ratio > 0.05:
                if old_track.actually_consistent():
                    print('prune rejecting bad_count_ratio', bad_count_ratio, old_track.actual_ids())
                keep = False

            if keep:
                self.tracks.append(old_track)

        self.print_track_actuals('prune')
