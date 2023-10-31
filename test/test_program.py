from http import HTTPStatus

import pytest

from welkin import Client
from welkin.exceptions import WelkinHTTPError
from welkin.models import Patient, Program, ProgramPhase, ProgramPhases, Programs
from welkin.models.formation import Program as FormationProgram


@pytest.mark.vcr
class TestProgram:
    @pytest.fixture
    def formation(self, client: Client) -> FormationProgram:
        return client.Formation().Programs().get()[0]

    @pytest.fixture
    def first_phase(self, formation) -> str:
        return formation.phases[0]["name"]

    @pytest.fixture
    def second_phase(self, formation) -> str:
        return formation.phases[1]["name"]

    @pytest.fixture
    def program(
        self,
        patient: Patient,
        formation: FormationProgram,
        first_phase: str,
        fixture_cassette,
    ) -> Program:
        program = patient.Program(programName=formation.name)

        with fixture_cassette():
            try:
                program = program.get()
            except WelkinHTTPError as exc:
                if exc.response.status_code != HTTPStatus.NOT_FOUND:
                    raise

                return program.update(assigned=True, phaseName=first_phase)

            if len(program.pathHistory) > 1:
                program.delete()
                program = program.update(assigned=True, phaseName=first_phase)

            return program

    @pytest.mark.parametrize(
        "identifier",
        [
            "id",
            "programName",
        ],
    )
    def test_read(self, patient: Patient, program: Program, identifier: str):
        prog = patient.Program(**{identifier: getattr(program, identifier)}).get()

        assert isinstance(prog, Program)
        assert isinstance(prog.currentPhase, ProgramPhase)
        assert isinstance(prog.pathHistory, ProgramPhases)

        assert prog.id == program.id

    def test_read_no_id(self, client):
        with pytest.raises(ValueError):
            client.Patient(id="notarealid").Program().get()

    def test_update(self, patient: Patient, program: Program, second_phase: str):
        assert program.currentPhase.name != second_phase
        assert len(program.pathHistory) == 1

        prog = patient.Program(programName=program.programName).update(
            phaseName=second_phase
        )
        assert prog.currentPhase.name == second_phase
        assert prog.currentPhase.name != program.currentPhase.name
        assert len(prog.pathHistory) == 2

    def test_delete(self, patient: Patient, program: Program):
        prog = patient.Program(id=program.id)
        prog.delete()

        with pytest.raises(WelkinHTTPError) as excinfo:
            prog.get()

        assert excinfo.value.response.status_code == 404


@pytest.mark.vcr
class TestPrograms:
    def test_read(self, patient):
        programs = patient.Programs().get()

        assert isinstance(programs, Programs)
        assert isinstance(programs[0], Program)
