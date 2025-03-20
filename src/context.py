from downtimes.persistence import DowntimesPersistence
from downtimes.service import DowntimesService


class ApplicationContext():
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ApplicationContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._downtimes_persistence = DowntimesPersistence()
        self.downtimes = DowntimesService(
            self._downtimes_persistence)
