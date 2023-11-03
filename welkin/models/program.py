from welkin.models.base import Collection, Resource
from welkin.models.util import find_patient_id_in_parents
from welkin.pagination import MetaInfoIterator


class ProgramPhase(Resource):
    pass


class ProgramPhases(Collection):
    resource = ProgramPhase


class PatientProgram(Resource):
    subresources = [ProgramPhase]
    nested_objects = {
        "phases": "ProgramPhase",
        "currentPhase": "ProgramPhase",
        "pathHistory": "ProgramPhases",
    }

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
        if hasattr(self, "id"):
            path += f"/history/{self.id}"
        elif hasattr(self, "programName"):
            path += f"/current/{self.programName}"
        else:
            raise ValueError("Program must have either programName or id attributes")

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
            f"{self._client.instance}/patients/{patient_id}/programs/{self.id}"
        )


class PatientPrograms(Collection):
    resource = PatientProgram
    iterator = MetaInfoIterator

    def get(
        self,
        patient_id: str = None,
        assigned_programs: bool = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
        patient_id = patient_id or find_patient_id_in_parents(self)

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/programs",
            params={
                "assignedPrograms": assigned_programs,
                "sort": sort,
            },
            *args,
            **kwargs,
        )
