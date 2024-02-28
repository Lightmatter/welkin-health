from io import BytesIO

from welkin.models.base import Collection, Resource
from welkin.pagination import PageableIterator
from welkin.util import model_id


class DocumentSummaryFile(Resource):
    @model_id("Patient", "DocumentSummary")
    def get(self, patient_id: str, document_summary_id: str) -> BytesIO:
        response = self._client.get(
            f"{self._client.instance}/patients/{patient_id}/document-summary/"
            f"{document_summary_id}/files/{self.id}"
        )

        return BytesIO(response)


class DocumentSummaryFiles(Collection):
    resource = DocumentSummaryFile
    iterator = PageableIterator

    @model_id("Patient", "DocumentSummary")
    def create(
        self,
        patient_id: str,
        document_summary_id: str,
        files: list = None,
        *args,
        **kwargs,
    ):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/document-summary/"
            f"{document_summary_id}/files",
            files=files,
            *args,
            **kwargs,
        )


class DocumentSummary(Resource):
    subresources = [DocumentSummaryFile, DocumentSummaryFiles]

    @model_id("Patient")
    def get(self, patient_id: str):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )

    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/document-summary"
        )

    @model_id("Patient")
    def delete(self, patient_id: str):
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )


class DocumentSummaries(Collection):
    resource = DocumentSummary
    iterator = PageableIterator

    @model_id("Patient")
    def get(self, patient_id: str, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/document-summary",
            *args,
            **kwargs,
        )
