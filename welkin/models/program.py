from welkin.models.base import Collection, Resource
from welkin.models.util import find_patient_id_in_parents
from welkin.pagination import PageIterator


class ProgramPhase(Resource):
    def update(self, patient_id: str = None, program_name: str = None, **kwargs):
        patient_id = patient_id or find_patient_id_in_parents(self)
        program_name = program_name or self._parent.name

        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/programs/"
            f"{program_name or self._parent.name}/phases",
            kwargs,
        )


class Program(Resource):
    subresources = [ProgramPhase]

    def get(
        self,
        patient_id: str = None,
        assigned_programs: bool = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
        patient_id = patient_id or find_patient_id_in_parents(self)

        path = f"{self._client.instance}/patients/{patient_id}/programs"
        if hasattr(self, "programName"):
            path += f"/current/{self.programName}"
        elif hasattr(self, "id"):
            path += f"/history/{self.id}"
        else:
            raise AttributeError("At least one of programName or id must be set.")

        return super().get(
            path,
            params={
                "assignedPrograms": assigned_programs,
                "sort": sort,
            },
            *args,
            **kwargs,
        )

    def update(self, patient_id: str = None, **kwargs):
        patient_id = patient_id or find_patient_id_in_parents(self)

        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/programs/"
            f"{self.programName}",
            kwargs,
        )

    def delete(self, patient_id: str = None):
        patient_id = patient_id or find_patient_id_in_parents(self)

        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/programs/"
            f"{self.programName}"
        )
