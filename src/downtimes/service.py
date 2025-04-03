from downtimes.persistence import DowntimesPersistence


class DowntimesService():
    def __init__(self, persistence: DowntimesPersistence):
        self._downtimes = persistence

    def get_events(self, user_guid: str, url: str, type: str, start_date: str, end_date: str):
        return self._downtimes.get_events(user_guid, url, type, start_date, end_date)

    def get_downtimes(self, user_guid: str, url: str, type: str):
        return self._downtimes.get_downtimes(user_guid, url, type)
