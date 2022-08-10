import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.assessment import AssessmentRecord, AssessmentRecords


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


@pytest.mark.vcr()
def test_assessment_record_get(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    assmt_record = patient.AssessmentRecord(
        id="c8764b19-ffa3-406a-b446-c971036a7a1d"
    ).get()

    assert isinstance(assmt_record, AssessmentRecord)
    assert assmt_record.id == "c8764b19-ffa3-406a-b446-c971036a7a1d"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_assessment_record_get_w_patient_id(client, vcr_cassette):
    assmt_record = client.AssessmentRecord(
        id="c8764b19-ffa3-406a-b446-c971036a7a1d"
    ).get(patient_id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    assert isinstance(assmt_record, AssessmentRecord)
    assert assmt_record.id == "c8764b19-ffa3-406a-b446-c971036a7a1d"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_assessment_record_update(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    assmt_record = patient.AssessmentRecord(
        id="e18a2759-5089-44e7-9d31-cf942476ffab"
    ).get()
    status = assmt_record.status

    assmt_record.status = "COMPLETED"
    assmt_record.update()

    assert assmt_record.status != status
    assert assmt_record.status == "COMPLETED"
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_assessment_record_create(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")
    assmt_record = patient.AssessmentRecord(assessmentName="asm-hello-form2").create()

    assert isinstance(assmt_record, AssessmentRecord)
    assert hasattr(assmt_record, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_assessment_record_delete(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    assmt_record = patient.AssessmentRecord(id="4f44ef74-9c82-4174-902b-1f9efebdebb7")

    assmt_record.delete()

    with pytest.raises(WelkinHTTPError) as excinfo:
        assmt_record.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_assessment_records_get(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    assmt_records = patient.AssessmentRecords().get()

    assert isinstance(assmt_records, AssessmentRecords)
    assert isinstance(assmt_records[0], AssessmentRecord)
    if len(assmt_records) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr(vcr_cassette_name="test_assessment_records_get_patient_id.yaml")
def test_assessment_records_get_patient_id(client, vcr_cassette):
    assmt_records = client.AssessmentRecords().get(
        patient_id="371dd15c-cedc-4425-a394-d666c8d3fc01"
    )

    assert isinstance(assmt_records, AssessmentRecords)
    assert isinstance(assmt_records[0], AssessmentRecord)
    if len(assmt_records) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"
