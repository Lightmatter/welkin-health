import pytest

from welkin.models import (
    AssessmentFormation,
    AssessmentFormations,
    CDTFormation,
    CDTFormations,
    DocumentTypeFormation,
    DocumentTypeFormations,
    EncounterDispositionFormation,
    EncounterFormation,
    EncounterFormations,
    GoalFormation,
    GoalFormations,
)


@pytest.mark.vcr
def test_assessment_formations_read(client, vcr_cassette):
    assessment_formations = client.AssessmentFormations().get()

    assert isinstance(assessment_formations, AssessmentFormations)
    assert isinstance(assessment_formations[0], AssessmentFormation)

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_assessment_formation_read(client, vcr_cassette):
    assessment_template = client.AssessmentFormation(name="asm-coaching-notes").get()

    assert isinstance(assessment_template, AssessmentFormation)
    assert assessment_template.name == "asm-coaching-notes"

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_cdt_formations_read(client, vcr_cassette):
    cdt_formations = client.CDTFormations().get()

    assert isinstance(cdt_formations, CDTFormations)
    assert isinstance(cdt_formations[0], CDTFormation)

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_cdt_formation_read(client, vcr_cassette):
    cdt_template = client.CDTFormation(name="allergies").get()

    assert isinstance(cdt_template, CDTFormation)
    assert cdt_template.name == "allergies"

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_document_type_formation_read(client, vcr_cassette):
    document_type = client.DocumentTypeFormation(name="doc-type-others").get()

    assert isinstance(document_type, DocumentTypeFormation)
    assert document_type.name == "doc-type-others"

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_document_types_formation_read(client, vcr_cassette):
    document_types = client.DocumentTypeFormations().get()

    assert isinstance(document_types, DocumentTypeFormations)
    assert isinstance(document_types[0], DocumentTypeFormation)

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_encounter_formations_read(client, vcr_cassette):
    encounter_formations = client.EncounterFormations().get()

    assert isinstance(encounter_formations, EncounterFormations)
    assert isinstance(encounter_formations[0], EncounterFormation)

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_encounter_formation_read(client, vcr_cassette):
    encounter_template = client.EncounterFormation(
        name="etmp-coaching-introduction"
    ).get()

    assert isinstance(encounter_template, EncounterFormation)
    assert encounter_template.name == "etmp-coaching-introduction"

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_encounter_disposition_formation_read(client, vcr_cassette):
    encounter_disposition_formation = client.EncounterDispositionFormation().get()

    assert isinstance(encounter_disposition_formation, EncounterDispositionFormation)
    assert encounter_disposition_formation.name == "__encounter_disposition__"

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_goal_formations_read(client, vcr_cassette):
    goal_templates = client.GoalFormations().get()

    assert isinstance(goal_templates, GoalFormations)
    assert isinstance(goal_templates[0], GoalFormation)

    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_goal_formation_read(client, vcr_cassette):
    goal_template = client.GoalFormation(name="eat-fruit").get()

    assert isinstance(goal_template, GoalFormation)
    assert goal_template.name == "eat-fruit"

    assert len(vcr_cassette) == 1
