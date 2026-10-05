from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from welkin.models import Task

if TYPE_CHECKING:
    from welkin.models import Patient

ASSIGNEE_ID = "d9925247-7505-464a-b42c-25ac71408494"


@pytest.mark.vcr
def test_task_create(client, patient: Patient, utc_datetime, vcr_cassette):
    task = client.Task(
        name="Test Task",
        description="Created by the welkin test suite",
        priority="HIGH",
        status="TODO",
        dueDate=utc_datetime,
        assignee={"id": ASSIGNEE_ID},
        patient={"id": patient.id},
    ).create()

    assert isinstance(task, Task)
    assert task.id
    assert task.name == "Test Task"
    assert task.priority == "HIGH"
    assert task.status == "TODO"
    assert task.assignee["id"] == ASSIGNEE_ID
    assert task.patient["id"] == patient.id
    assert len(vcr_cassette) == 1
