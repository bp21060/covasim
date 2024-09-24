class Event:
    def __init__(self, event_type="n_exposed", threshold=20, min_age=0, max_age=None):
        self.event_type = event_type
        self.threshold = threshold
        self.min_age = min_age
        self.max_age = max_age