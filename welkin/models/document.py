from welkin.models.base import Collection, Resource
from welkin.models.util import find_patient_id_in_parents
from welkin.pagination import PageableIterator


class DocumentSummaryFile(Resource):
    def get(self, patient_id: str = None, document_summary_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not document_summary_id:
            document_summary_id = self._parent.id

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{document_summary_id}/files/{self.id}"
        )

    def create(self, patient_id: str = None, document_summary_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not document_summary_id:
            document_summary_id = self._parent.id

        return super().post(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{document_summary_id}/files"
        )


class DocumentSummary(Resource):
    subresources = [DocumentSummaryFile]

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
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )

    def update(self, patient_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().put(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )

    def delete(self, patient_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/document-summary/{self.id}"
        )


class Documents(Collection):
    resource = DocumentSummary
    iterator = PageableIterator

    def get(self, patient_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/document-summary"
        )
