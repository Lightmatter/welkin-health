from datetime import datetime, timezone
from enum import Enum

from welkin.models.base import Collection, Resource
from welkin.util import clean_datetime


class CalendarEvent(Resource):
    def __str__(self):
        try:
            return f"{self.firstName} {self.lastName}"
        except AttributeError:
            return self.username

    def create(self):
        return super().post("admin/users")

    def get(self):
        return super().get(f"{self._client.instance}/calendar/events/{self.id}")

    def update(self, **kwargs):
        return super().patch(f"admin/users/{self.username}", kwargs)

    def delete(self):
        return super().delete(f"admin/users/{self.id}", params=dict(type="ID"))


class EventType(Enum):
    GROUP_THERAPY = "GROUP_THERAPY"
    APPOINTMENT = "APPOINTMENT"
    LEAVE = "LEAVE"
    ENCOUNTER = "ENCOUNTER"


class EventStatus(Enum):
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"


class EventMode(Enum):
    IN_PERSON = "IN-PERSON"
    CALL = "CALL"
    VIDEO = "VIDEO"


class CalendarEvents(Collection):
    resource = CalendarEvent

    def get(
        self,
        from_date: datetime,
        to_date: datetime,
        participant_ids: list = None,
        event_type: str = None,
        sort: str = None,
        include_cancelled: bool = None,
        include_encounter_info: bool = None,
        exclude_assigned_to_encounter_events: bool = None,
        viewer_timezone: str = None,
    ):
        params = {
            "from": from_date,
            "to": to_date,
            "participantIds": participant_ids,
            "eventType": event_type,
            "sort": sort,
            "includeCancelled": include_cancelled,
            "includeEncounterInfo": include_encounter_info,
            "excludeAssignedToEncounterEvents": exclude_assigned_to_encounter_events,
            "viewerTimezone": viewer_timezone,
        }

        return super().get(f"{self._client.instance}/calendar/events", params=params)
