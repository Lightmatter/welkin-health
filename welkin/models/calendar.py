from datetime import datetime, timezone
from enum import Enum

from welkin.models.base import Collection, Resource


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


class Days(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


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


class WorkHours(Resource):
    @property
    def id(self):
        return self.details[0]["workHoursId"]

    @id.setter
    def id(self, value):
        if not hasattr(self, "details"):
            self.details = [{}]

        self.details[0]["workHoursId"] = value

    def create(self, repeating=True):
        self.startDateTime = datetime.now(tz=timezone.utc)
        if repeating:
            self.endDateTime = self.startDateTime.replace(
                year=self.startDateTime.year + 50
            )

        return super().post(f"{self._client.instance}/calendar/work-hours")

    def get(self):
        return super().get(f"{self._client.instance}/calendar/work-hours/{self.id}")

    def update(self, **kwargs):
        return super().put(
            f"{self._client.instance}/calendar/work-hours/{self.id}", kwargs
        )


class WorkerHours(Collection):
    resource = WorkHours

    def get(
        self,
        from_date: datetime,
        to_date: datetime,
        ids: list = None,
        timezone: str = None,
    ):
        params = {
            "psmIds": ids,
            "from": from_date,
            "to": to_date,
            "timezone": timezone,
        }

        return super().get(
            f"{self._client.instance}/calendar/work-hours", params=params
        )
