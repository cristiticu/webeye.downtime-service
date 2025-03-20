from downtimes.exceptions import CurrentStatusNotFound
from downtimes.model import DowntimePeriod, DowntimeEvent, CurrentStatus
import settings
from shared.dynamodb import dynamodb_table
from boto3.dynamodb.conditions import Key


class DowntimesPersistence():
    def __init__(self):
        self.downtimes = dynamodb_table(settings.DOWNTIMES_TABLE_NAME)

    def persist(self, payload: DowntimeEvent | CurrentStatus | DowntimePeriod):
        self.downtimes.put_item(Item=payload.to_db_item())

    def get_events(self, user_guid: str, url: str, type: str, start_date: str, end_date: str):
        h_key = f"{user_guid}#{url}#{type}"
        low = f"EVENT#{start_date}"
        high = f"EVENT#{end_date}"

        response = self.downtimes.query(
            KeyConditionExpression=Key("h_key").eq(h_key) & Key("s_key").between(low, high))
        items = response.get("Items")

        return [DowntimeEvent.from_db_item(item) for item in items]

    def get_downtimes(self, user_guid: str, url: str, type: str):
        h_key = f"{user_guid}#{url}#{type}"

        response = self.downtimes.query(
            KeyConditionExpression=Key("h_key").eq(h_key) & Key("s_key").begins_with("DOWNTIME"))
        items = response.get("Items")

        return [DowntimePeriod.from_db_item(item) for item in items]

    def get_current_status(self, user_guid: str, url: str, type: str):
        h_key = f"{user_guid}#{url}#{type}"

        response = self.downtimes.get_item(
            Key={"h_key": h_key, "s_key": "CURRENT"})
        item = response.get("Item")

        if item is None:
            raise CurrentStatusNotFound()

        return CurrentStatus.from_db_item(item)

    def delete(self,  user_guid: str, url: str, type: str):
        h_key = f"{user_guid}#{url}#{type}"
        self.downtimes.delete_item(Key={"h_key": h_key})
