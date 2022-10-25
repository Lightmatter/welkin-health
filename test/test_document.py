from io import BytesIO

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.document import (
    Documents,
    DocumentSummary,
    DocumentSummaryFile,
    DocumentSummaryFiles,
)


@pytest.mark.vcr()
def test_documents_get_patient_id(client, vcr_cassette):
    documents = client.Documents().get(
        patient_id="28fd23be-7530-4257-8adb-927e07af9d5d"
    )

    assert isinstance(documents, Documents)
    assert isinstance(documents[0], DocumentSummary)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_documents_subresource(client, vcr_cassette):
    documents = (
        client.Patient(id="28fd23be-7530-4257-8adb-927e07af9d5d").Documents().get()
    )

    assert isinstance(documents, Documents)
    assert isinstance(documents[0], DocumentSummary)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_document_summary_get(client, vcr_cassette):
    document = (
        client.Patient(id="28fd23be-7530-4257-8adb-927e07af9d5d")
        .DocumentSummary(id="a7ca862d-44c9-494a-a2b9-9490c0305bbd")
        .get()
    )

    assert isinstance(document, DocumentSummary)
    assert document.id == "a7ca862d-44c9-494a-a2b9-9490c0305bbd"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_document_summary_delete(client, vcr_cassette):
    document = client.Patient(
        id="28fd23be-7530-4257-8adb-927e07af9d5d"
    ).DocumentSummary(id="a7ca862d-44c9-494a-a2b9-9490c0305bbd")

    document.delete()

    with pytest.raises(WelkinHTTPError) as excinfo:
        document.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_document_summary_create(client, vcr_cassette):
    document = (
        client.Patient(id="28fd23be-7530-4257-8adb-927e07af9d5d")
        .DocumentSummary(type="doc-type-others")
        .create()
    )

    assert isinstance(document, DocumentSummary)
    assert hasattr(document, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
@pytest.mark.xfail("https://github.com/kevin1024/vcrpy/issues/660")
def test_document_summary_files_create(client, vcr_cassette):

    with open("test/walrus_uJGKbRm.jpeg", "rb") as f:
        files = client.DocumentSummaryFiles().create(
            patient_id="28fd23be-7530-4257-8adb-927e07af9d5d",
            document_summary_id="909c7488-7a5e-4e87-b6f2-606e8306b4b6",
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


@pytest.mark.vcr()
def test_document_summary_file_get(client, vcr_cassette):
    doc_summary = (
        client.Patient(id="28fd23be-7530-4257-8adb-927e07af9d5d")
        .DocumentSummary(id="909c7488-7a5e-4e87-b6f2-606e8306b4b6")
        .DocumentSummaryFile(id="3c689f3b-abd3-4b15-81a0-50507a45340d")
    )
    file = doc_summary.get()

    assert isinstance(file, BytesIO)
    assert isinstance(doc_summary, DocumentSummaryFile)
    assert doc_summary.file == file
    assert len(vcr_cassette) == 1
