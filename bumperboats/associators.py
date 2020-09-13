from bumperboats.track import SimpleSecondOrderKFTrack


class FakeAssociator:
    def __init__(self):
        self.track_map = {}

    def on_data(self, contacts):
        for contact in contacts:
            track = self.track_map.setdefault(contact.actual_id, SimpleSecondOrderKFTrack(dt=1, std=3))
            track.on_data(contact.measurement)


    def print_diagnostics(self):
        for track_id, track in self.track_map.items():
            track.print_diagnostics()
