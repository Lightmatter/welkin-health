from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from welkin.models import Task, Tasks

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


@pytest.mark.vcr
def test_task_read(client, vcr_cassette):
    task = client.Tasks().get(params={"size": 1})[0]
    fetched = client.Task(id=task.id).get()

    assert isinstance(fetched, Task)
    assert fetched.id == task.id
    assert fetched.name == task.name
    assert len(vcr_cassette) == 2


@pytest.mark.vcr
def test_tasks_read(client, vcr_cassette):
    tasks = client.Tasks().get(params={"assigneeIds": [ASSIGNEE_ID]})

    assert isinstance(tasks, Tasks)
    assert all(isinstance(t, Task) for t in tasks)
    assert all(t.assignee["id"] == ASSIGNEE_ID for t in tasks)
    assert len(vcr_cassette) == 1
