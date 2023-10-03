from welkin.models.base import Collection, Resource
from welkin.models.util import find_patient_id_in_parents
from welkin.pagination import PageIterator


class ProgramPhases(Resource):
    def _url(self, patient_id: str = None, program_name: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not program_name:
            program_name = self._parent.name

        return f"{self._client.instance}/patients/{patient_id}/programs/{program_name}/phases"

    def update(self, phase_name: str, patient_id: str = None, program_name: str = None):
        return super().patch(
            self._url(patient_id, program_name), {"phaseName": phase_name}
        )


class Program(Resource):
    subresources = [ProgramPhases]

    def _url(self, patient_id: str = None, program_name: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not program_name:
            program_name = self.name

        return f"{self._client.instance}/patients/{patient_id}/programs/{program_name}"

    def delete(self, patient_id: str = None, program_name: str = None):
        return super().delete(self._url(patient_id, program_name))

    def update(
        self,
        patient_id: str = None,
        program_name: str = None,
    ):
        return super().patch(
            self._url(patient_id, program_name),
            {"assigned": True, "status": "IN_PROGRESS"},
        )


class CurrentPrograms(Collection):
    resource = Program
    iterator = PageIterator

    def _url(self, patient_id: str = None, program_name: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not program_name:
            raise ValueError("A program name must be provided.")

        return f"{self._client.instance}/patients/{patient_id}/programs/current/{program_name}"

    def get(
        self,
        patient_id: str = None,
        program_name: str = None,
        assigned_programs: bool = None,
        sort: str = None,
        **kwargs,
    ):
        return super().get(
            self._url(patient_id, program_name),
            params={
                "assignedPrograms": assigned_programs,
                "sort": sort,
            },
        )


class ProgramHistory(Resource):
    resource = Program
    iterator = PageIterator

    def _url(self, patient_id: str = None, program_id: str = None):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        if not program_id:
            raise ValueError("A program ID must be provided.")

        return f"{self._client.instance}/patients/{patient_id}/programs/history/{program_id}"

    def get(
        self,
        patient_id: str = None,
        program_id: str = None,
        assigned_programs: bool = None,
        sort: str = None,
    ):
        if not patient_id:
            patient_id = find_patient_id_in_parents(self)

        params = {
            "assignedPrograms": assigned_programs,
            "sort": sort,
        }
        return super().get(
            self._url(patient_id, program_id),
            params=params,
        )
