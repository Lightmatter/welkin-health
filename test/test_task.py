from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from welkin.models import Task, Tasks

if TYPE_CHECKING:
    from datetime import datetime

    from vcr.cassette import Cassette

    from welkin import Client
    from welkin.models import Patient, User


@pytest.mark.vcr
def test_task_create(
    client: Client,
    patient: Patient,
    user: User,
    utc_datetime: datetime,
    vcr_cassette: Cassette,
):
    task = client.Task(
        name="Test Task",
        description="Created by the welkin test suite",
        priority="HIGH",
        status="TODO",
        dueDate=utc_datetime,
        assignee={"id": user.id},
        patient={"id": patient.id},
    ).create()

    assert isinstance(task, Task)
    assert task.id
    assert task.name == "Test Task"
    assert task.priority == "HIGH"
    assert task.status == "TODO"
    assert task.assignee["id"] == user.id
    assert task.patient["id"] == patient.id
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_task_read(client: Client, vcr_cassette: Cassette):
    tasks = client.Tasks().get()
    task = tasks[0]
    fetched = client.Task(id=task.id).get()

    assert isinstance(fetched, Task)
    assert fetched.id == task.id
    assert fetched.name == task.name
    assert len(vcr_cassette) == 2


@pytest.mark.vcr
def test_task_read_all(client: Client, user: User, vcr_cassette: Cassette):
    tasks = client.Tasks().get(params={"assigneeIds": [user.id]})

    assert isinstance(tasks, Tasks)
    assert all(isinstance(t, Task) for t in tasks)
    assert all(t.assignee["id"] == user.id for t in tasks)
    assert len(vcr_cassette) == 1
