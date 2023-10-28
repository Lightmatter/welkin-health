from datetime import date

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models import Program, ProgramPhase


@pytest.fixture
def program(client):
    return client.Formation().Programs().get()[0]


@pytest.fixture
def assigned_program(patient, program):
    phase = program.phases[0]["name"]
    return patient.Program(programName=program.name).update(
        assigned=True, phaseName=phase
    )


@pytest.mark.vcr
def test_program_read(patient, assigned_program, vcr_cassette):
    program = patient.Program(programName=assigned_program.programName).get()

    assert isinstance(program, Program)
    assert program.id == assigned_program.id
    assert len(vcr_cassette) == 4


@pytest.mark.vcr
def test_program_update(client, patient, vcr_cassette):
    program = client.Program(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd").get()
    name = program.firstName

    program.update(firstName="Baz")

    assert program.firstName != name
    assert len(vcr_cassette) == 2


@pytest.mark.vcr
def test_program_delete(client, patient, vcr_cassette):
    program = client.Program(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd")

    with pytest.raises(WelkinHTTPError) as excinfo:
        program.delete()

    assert excinfo.value.response.status_code == 403

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_program_phase_update(client, patient, vcr_cassette):
    program = client.Program(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd").get()
    name = program.firstName

    program.update(firstName="Baz")

    assert program.firstName != name
    assert len(vcr_cassette) == 2
