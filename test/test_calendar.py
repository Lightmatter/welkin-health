from datetime import datetime, timedelta, timezone

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.calendar import CalendarEvent, CalendarEvents, Schedule, Schedules

UTC = timezone.utc


@pytest.mark.vcr()
def test_calendar_event_create(client, vcr_cassette):
    start = datetime.now(tz=UTC) + timedelta(hours=6)
    end = start + timedelta(hours=1)

    event = client.CalendarEvent(
        startDateTime=start,
        endDateTime=end,
        hostId="d9925247-7505-464a-b42c-25ac71408494",
        participants=[
            {
                "participantId": "d9925247-7505-464a-b42c-25ac71408494",
                "participantRole": "psm",
            }
        ],
    ).create()

    assert isinstance(event, CalendarEvent)
    assert hasattr(event, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_calendar_event_read(client, vcr_cassette):
    event_id = "9386a88a-467e-4144-a7df-1af12d6d5aaf"
    calendar = client.CalendarEvent(id=event_id).get()

    assert isinstance(calendar, CalendarEvent)
    assert calendar.id == event_id
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_calendar_event_read_all(client, vcr_cassette):
    from_date = datetime(2022, 4, 1, 16, 38, 20, 641000, tzinfo=UTC)
    to_date = datetime(2022, 6, 30, 16, 38, 20, 641000, tzinfo=UTC)

    events = client.CalendarEvents().get(from_date, to_date, include_cancelled=True)

    assert isinstance(events, CalendarEvents)
    assert isinstance(events[0], CalendarEvent)

    if len(events) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_calendar_event_update(client, vcr_cassette):
    event = client.CalendarEvent(id="f7fc881d-28af-4fe1-b2ff-20e1ca33982f").get()
    title = event.eventTitle

    event.update(eventTitle="New event title")

    assert event.eventTitle != title
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_calendar_event_delete(client, vcr_cassette):
    event = client.CalendarEvent(id="f7fc881d-28af-4fe1-b2ff-20e1ca33982f").get()
    event.delete()

    if event.startDateTime <= datetime.now(tz=UTC).isoformat():
        event.get()
        assert event.eventStatus == "CANCELLED"

    else:
        with pytest.raises(WelkinHTTPError) as excinfo:
            event.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 3


@pytest.mark.vcr()
def test_schedule_read_all(client, vcr_cassette):
    from_date = datetime(2022, 4, 1, 16, 38, 20, 641000, tzinfo=UTC)
    to_date = datetime(2022, 6, 30, 16, 38, 20, 641000, tzinfo=UTC)

    schedules = client.Schedules().get(
        ids=["d9925247-7505-464a-b42c-25ac71408494"],
        from_date=from_date,
        to_date=to_date,
        include_cancelled=True,
    )

    assert isinstance(schedules, Schedules)
    assert isinstance(schedules[0], Schedule)

    assert len(vcr_cassette) == 1
