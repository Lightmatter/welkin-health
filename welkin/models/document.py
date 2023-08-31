from io import BytesIO

from welkin.models.base import Collection, Resource
from welkin.models.util import find_patient_id_in_parents
from welkin.pagination import PageableIterator


class DocumentSummaryFile(Resource):
    def get(self, patient_id: str = None, document_summary_id: str = None) -> BytesIO:
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not document_summary_id:
            document_summary_id = self._parent.id

        content = self._client.get(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{document_summary_id}/files/{self.id}"
        )

        return BytesIO(content)


class DocumentSummaryFiles(Collection):
    resource = DocumentSummaryFile
    iterator = PageableIterator

    def create(
        self,
        patient_id: str = None,
        document_summary_id: str = None,
        files: list = None,
        *args,
        **kwargs,
    ):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not document_summary_id:
            document_summary_id = self._parent.id

        return super().post(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{document_summary_id}/files",
            files=files,
            *args,
            **kwargs,
        )


class DocumentSummary(Resource):
    subresources = [DocumentSummaryFile, DocumentSummaryFiles]

    def get(self, patient_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )

    def create(self, patient_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().post(
            f"{self._client.instance}/patients/{patient_id}/document-summary"
        )

    def delete(self, patient_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )


class DocumentSummaries(Collection):
    resource = DocumentSummary
    iterator = PageableIterator

    def get(self, patient_id: str = None, *args, **kwargs):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/document-summary",
            *args,
            **kwargs,
        )
