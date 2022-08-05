import pytest

from welkin.models.assessment import AssessmentRecord, AssessmentRecordAnswers
from welkin.models.patient import Patient


@pytest.mark.vcr()
def test_assessment_record_answers_update(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    assmt_record = patient.AssessmentRecord(
        id="c8764b19-ffa3-406a-b446-c971036a7a1d"
    ).get()
    hi_answer = assmt_record.answers["cdt-hello__cdtf-hi"]
    assmt_record.AssessmentRecordAnswers(**{"cdt-hello__cdtf-hi": "abc123def"}).update()
    assmt_record = patient.AssessmentRecord(
        id="c8764b19-ffa3-406a-b446-c971036a7a1d"
    ).get()

    assert assmt_record.answers["cdt-hello__cdtf-hi"] == "abc123def"
    assert hi_answer != assmt_record.answers["cdt-hello__cdtf-hi"]
    assert len(vcr_cassette) == 3
