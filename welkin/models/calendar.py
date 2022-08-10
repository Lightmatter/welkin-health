from datetime import datetime
from enum import Enum

from welkin.models.base import Collection, Resource
from welkin.pagination import PageableIterator


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


class CalendarEvent(Resource):
    def create(self):
        # TODO: Accept User and Patient instances as participants
        return super().post(f"{self._client.instance}/calendar/events")

    def get(self):
        return super().get(f"{self._client.instance}/calendar/events/{self.id}")

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/calendar/events/{self.id}", kwargs
        )

    def delete(self):
        return super().delete(f"{self._client.instance}/calendar/events/{self.id}")


class CalendarEvents(Collection):
    resource = CalendarEvent
    iterator = PageableIterator

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
        # Validation
        if event_type:
            EventType(event_type)

        # IDEA: Consider inferring params from instance properties
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


class Schedule(Resource):
    pass


class Schedules(Collection):
    resource = Schedule
    iterator = PageableIterator

    def get(
        self,
        ids: list,
        from_date: datetime,
        to_date: datetime,
        include_cancelled: bool = None,
        available: bool = False,
        full: bool = False,
    ):
        route = "psm-schedules"
        if available:
            route = "available-psm-schedules"
        if full:
            route = "full-psm-schedules"

        params = {
            "psmIds": ids,
            "from": from_date,
            "to": to_date,
            "includeCancelled": include_cancelled,
        }

        return super().get(f"{self._client.instance}/calendar/{route}", params=params)
