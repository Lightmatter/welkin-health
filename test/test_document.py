from io import BytesIO

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models import (
    DocumentSummaries,
    DocumentSummary,
    DocumentSummaryFile,
    DocumentSummaryFiles,
)


@pytest.mark.vcr
def test_document_summaries_get_patient_id(client, vcr_cassette):
    documents = client.DocumentSummaries().get(
        patient_id="283f50d3-0840-426f-b07b-bd8e4ab76401"
    )

    assert isinstance(documents, DocumentSummaries)
    assert isinstance(documents[0], DocumentSummary)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_document_summaries_subresource(client, vcr_cassette):
    documents = (
        client.Patient(id="283f50d3-0840-426f-b07b-bd8e4ab76401")
        .DocumentSummaries()
        .get()
    )

    assert isinstance(documents, DocumentSummaries)
    assert isinstance(documents[0], DocumentSummary)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_document_summary_get(client, vcr_cassette):
    document = (
        client.Patient(id="283f50d3-0840-426f-b07b-bd8e4ab76401")
        .DocumentSummary(id="5106ec9d-da83-4ce6-89d0-6a9b7fde0138")
        .get()
    )

    assert isinstance(document, DocumentSummary)
    assert document.id == "5106ec9d-da83-4ce6-89d0-6a9b7fde0138"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_document_summary_delete(client, vcr_cassette):
    document = client.Patient(
        id="283f50d3-0840-426f-b07b-bd8e4ab76401"
    ).DocumentSummary(id="5106ec9d-da83-4ce6-89d0-6a9b7fde0138")

    document.delete()

    with pytest.raises(WelkinHTTPError) as excinfo:
        document.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 2


@pytest.mark.vcr
def test_document_summary_create(client, vcr_cassette):
    document = (
        client.Patient(id="283f50d3-0840-426f-b07b-bd8e4ab76401")
        .DocumentSummary(type="doc-type-others")
        .create()
    )

    assert isinstance(document, DocumentSummary)
    assert hasattr(document, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
@pytest.mark.skip(
    reason="the bytes upload hits this issue in vcr: https://github.com/kevin1024/vcrpy/issues/660 but this test shows the correct implementation"
)
def test_document_summary_files_create(client, vcr_cassette):
    with open("test/walrus_uJGKbRm.jpeg", "rb") as f:
        files = client.DocumentSummaryFiles().create(
            patient_id="283f50d3-0840-426f-b07b-bd8e4ab76401",
            document_summary_id="b3934cac-72dc-4a1e-9141-9b9f7c16eacd",
            files=[
                (
                    "files",
                    (
                        "picture.jpeg",
                        f,
                        "image/jpeg",
                    ),
                )
            ],
        )

    assert isinstance(files, DocumentSummaryFiles)
    assert isinstance(files[0], DocumentSummaryFile)
    assert hasattr(files[0], "id")
    assert files[0].originalName == "picture.jpeg"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_document_summary_file_get(client, vcr_cassette):
    doc_summary = (
        client.Patient(id="283f50d3-0840-426f-b07b-bd8e4ab76401")
        .DocumentSummary(id="b3934cac-72dc-4a1e-9141-9b9f7c16eacd")
        .DocumentSummaryFile(id="c5998e85-9f4b-41ad-9c97-d23981fd6c61")
    )
    file = doc_summary.get()

    assert isinstance(file, BytesIO)
    assert isinstance(doc_summary, DocumentSummaryFile)
    assert doc_summary.id == "c5998e85-9f4b-41ad-9c97-d23981fd6c61"
    assert len(vcr_cassette) == 1
