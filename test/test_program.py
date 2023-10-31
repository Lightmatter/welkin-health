from http import HTTPStatus

import pytest

from welkin import Client
from welkin.exceptions import WelkinHTTPError
from welkin.models import Patient, Program, ProgramPhase, ProgramPhases, Programs
from welkin.models.formation import Program as FormationProgram


@pytest.fixture
def formation(client: Client) -> FormationProgram:
    return client.Formation().Programs().get()[0]


@pytest.fixture
def first_phase(formation) -> str:
    return formation.phases[0]["name"]


@pytest.fixture
def second_phase(formation) -> str:
    return formation.phases[1]["name"]


@pytest.fixture
def model(patient: Patient, formation: FormationProgram, first_phase: str) -> Program:
    model = patient.Program(programName=formation.name)
    try:
        model = model.get()
    except WelkinHTTPError as exc:
        if exc.response.status_code != HTTPStatus.NOT_FOUND:
            raise

        return model.update(assigned=True, phaseName=first_phase)

    if len(model.pathHistory) > 1:
        model.delete()
        model = model.update(assigned=True, phaseName=first_phase)

    return model


@pytest.mark.vcr
class TestProgram:
    @pytest.mark.parametrize("identifier", ["id", "programName"])
    def test_read(self, patient: Patient, model: Program, identifier: str):
        program = patient.Program(**{identifier: getattr(model, identifier)}).get()

        assert isinstance(program, Program)
        assert isinstance(program.currentPhase, ProgramPhase)
        assert isinstance(program.pathHistory, ProgramPhases)

        assert program.id == model.id

    def test_update(self, patient: Patient, model: Program, second_phase: str):
        assert model.currentPhase.name != second_phase
        assert len(model.pathHistory) == 1

        program = patient.Program(programName=model.programName).update(
            phaseName=second_phase
        )
        assert program.currentPhase.name == second_phase
        assert program.currentPhase.name != model.currentPhase.name
        assert len(program.pathHistory) == 2

    def test_delete(self, patient: Patient, model: Program):
        program = patient.Program(id=model.id)
        program.delete()

        with pytest.raises(WelkinHTTPError) as excinfo:
            program.get()

        assert excinfo.value.response.status_code == 404


@pytest.mark.vcr
class TestPrograms:
    def test_read(self, patient):
        programs = patient.Programs().get()

        assert isinstance(programs, Programs)
        assert isinstance(programs[0], Program)
