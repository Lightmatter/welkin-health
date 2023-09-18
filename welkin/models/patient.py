from welkin.models.assessment import AssessmentRecord, AssessmentRecords
from welkin.models.base import Collection, Resource
from welkin.models.care_plan import CarePlan
from welkin.models.cdt import CDT, CDTs
from welkin.models.chat import Chat, Chats, SearchChats
from welkin.models.document import (
    DocumentSummaries,
    DocumentSummary,
    DocumentSummaryFile,
)
from welkin.models.email import Email, Emails
from welkin.models.encounter import Encounter, Encounters
from welkin.models.sms import SMS, SMSes
from welkin.pagination import PageableIterator


class Patient(Resource):
    subresources = [
        AssessmentRecord,
        AssessmentRecords,
        CarePlan,
        CDT,
        CDTs,
        Chat,
        Chats,
        DocumentSummaries,
        DocumentSummary,
        DocumentSummaryFile,
        Email,
        Emails,
        Encounter,
        Encounters,
        SearchChats,
        SMS,
        SMSes,
    ]

    def create(self):
        return super().post(f"{self._client.instance}/patients")

    def get(self):
        return super().get(f"{self._client.instance}/patients/{self.id}")

    def update(self, **kwargs):
        return super().patch(f"{self._client.instance}/patients/{self.id}", kwargs)

    def delete(self):
        return super().delete(f"{self._client.instance}/patients/{self.id}")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Patients(Collection):
    resource = Patient
    iterator = PageableIterator

    def get(self, filter={}, *args, **kwargs):
        # TODO: Add sort and query arguments.
        return super().post(
            f"{self._client.instance}/by-filter/patients", json=filter, *args, **kwargs
        )
