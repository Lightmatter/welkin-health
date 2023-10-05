import pytest

from welkin.models.formation import (
    CDT,
    Assessment,
    Assessments,
    CDTs,
    DocumentType,
    DocumentTypes,
    Encounter,
    EncounterDisposition,
    Encounters,
    Formation,
    Goal,
    Goals,
    Program,
    Programs,
)


class TestFormation:
    @pytest.fixture
    def formation(self, client) -> Formation:
        return client.Formation()

    @pytest.mark.vcr
    def test_assessments_read(self, formation, vcr_cassette):
        assessment_formations = formation.Assessments().get()

        assert isinstance(assessment_formations, Assessments)
        assert isinstance(assessment_formations[0], Assessment)

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_assessment_read(self, formation, vcr_cassette):
        assessment_template = formation.Assessment(name="asm-coaching-notes").get()

        assert isinstance(assessment_template, Assessment)
        assert assessment_template.name == "asm-coaching-notes"

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_cdts_read(self, formation, vcr_cassette):
        cdt_formations = formation.CDTs().get()

        assert isinstance(cdt_formations, CDTs)
        assert isinstance(cdt_formations[0], CDT)

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_cdt_read(self, formation, vcr_cassette):
        cdt_template = formation.CDT(name="allergies").get()

        assert isinstance(cdt_template, CDT)
        assert cdt_template.name == "allergies"

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_document_type_read(self, formation, vcr_cassette):
        document_type = formation.DocumentType(name="doc-type-others").get()

        assert isinstance(document_type, DocumentType)
        assert document_type.name == "doc-type-others"

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_document_types_read(self, formation, vcr_cassette):
        document_types = formation.DocumentTypes().get()

        assert isinstance(document_types, DocumentTypes)
        assert isinstance(document_types[0], DocumentType)

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_encounters_read(self, formation, vcr_cassette):
        encounter_formations = formation.Encounters().get()

        assert isinstance(encounter_formations, Encounters)
        assert isinstance(encounter_formations[0], Encounter)

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_encounter_read(self, formation, vcr_cassette):
        encounter_template = formation.Encounter(
            name="etmp-coaching-introduction"
        ).get()

        assert isinstance(encounter_template, Encounter)
        assert encounter_template.name == "etmp-coaching-introduction"

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_encounter_disposition_read(self, formation, vcr_cassette):
        encounter_disposition_formation = formation.EncounterDisposition().get()

        assert isinstance(encounter_disposition_formation, EncounterDisposition)
        assert encounter_disposition_formation.name == "__encounter_disposition__"

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_goals_read(self, formation, vcr_cassette):
        goal_templates = formation.Goals().get()

        assert isinstance(goal_templates, Goals)
        assert isinstance(goal_templates[0], Goal)

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_goal_read(self, formation, vcr_cassette):
        goal_template = formation.Goal(name="eat-fruit").get()

        assert isinstance(goal_template, Goal)
        assert goal_template.name == "eat-fruit"

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_programs_read(self, formation, vcr_cassette):
        programs = formation.Programs().get()

        assert isinstance(programs, Programs)
        assert isinstance(programs[0], Program)

        assert len(vcr_cassette) == 1

    @pytest.mark.vcr
    def test_program_read(self, formation, vcr_cassette):
        programs = formation.Program(name="prog-non-target-patient").get()

        assert isinstance(programs, Program)
        assert programs.name == "prog-non-target-patient"

        assert len(vcr_cassette) == 1
