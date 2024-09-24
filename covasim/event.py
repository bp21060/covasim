class Event:
    def __init__(self, measurement="n",condition="exposed", threshold=20, min_age=0, max_age=None):
        self.measurement = measurement
        self.condition = condition
        self.threshold = threshold
        self.min_age = min_age
        self.max_age = max_age