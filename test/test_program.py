from http import HTTPStatus

import pytest

from welkin import Client
from welkin.exceptions import WelkinHTTPError
from welkin.models import (
    Patient,
    PatientProgram,
    PatientPrograms,
    ProgramPhase,
    ProgramPhases,
)
from welkin.models.formation import Program


@pytest.mark.vcr
class TestProgram:
    @pytest.fixture
    def formation(self, client: Client) -> Program:
        return client.Formation().Programs().get()[0]

    @pytest.fixture
    def first_phase(self, formation) -> str:
        return formation.phases[0]["name"]

    @pytest.fixture
    def second_phase(self, formation) -> str:
        return formation.phases[1]["name"]

    @pytest.fixture
    def patient_program(
        self,
        patient: Patient,
        formation: Program,
        first_phase: str,
        fixture_cassette,
    ) -> PatientProgram:
        program = patient.PatientProgram(programName=formation.name)

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
    def test_read(
        self, patient: Patient, patient_program: PatientProgram, identifier: str
    ):
        prog = patient.PatientProgram(
            **{identifier: getattr(patient_program, identifier)}
        ).get()

        assert isinstance(prog, PatientProgram)
        assert isinstance(prog.currentPhase, ProgramPhase)
        assert isinstance(prog.pathHistory, ProgramPhases)

        assert prog.id == patient_program.id

    def test_read_no_id(self, client):
        with pytest.raises(ValueError):
            client.Patient(id="notarealid").PatientProgram().get()

    def test_update(
        self, patient: Patient, patient_program: PatientProgram, second_phase: str
    ):
        assert patient_program.currentPhase.name != second_phase
        assert len(patient_program.pathHistory) == 1

        prog = patient.PatientProgram(programName=patient_program.programName).update(
            phaseName=second_phase
        )
        assert prog.currentPhase.name == second_phase
        assert prog.currentPhase.name != patient_program.currentPhase.name
        assert len(prog.pathHistory) == 2

    def test_delete(self, patient: Patient, patient_program: PatientProgram):
        prog = patient.PatientProgram(id=patient_program.id)
        prog.delete()

        with pytest.raises(WelkinHTTPError) as excinfo:
            prog.get()

        assert excinfo.value.response.status_code == 404


@pytest.mark.vcr
class TestPrograms:
    def test_read(self, patient):
        programs = patient.PatientPrograms().get()

        assert isinstance(programs, PatientPrograms)
        assert isinstance(programs[0], PatientProgram)
