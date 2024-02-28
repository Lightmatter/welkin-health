from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator
from welkin.util import model_id


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

    @model_id("Patient")
    def get(
        self,
        patient_id: str,
        assigned_programs: bool = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
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

    @model_id("Patient")
    def update(self, patient_id: str, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/programs/"
            f"{self.programName}",
            kwargs,
        )

    @model_id("Patient")
    def delete(self, patient_id: str):
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/programs/{self.id}"
        )


class PatientPrograms(Collection):
    resource = PatientProgram
    iterator = MetaInfoIterator

    @model_id("Patient")
    def get(
        self,
        patient_id: str,
        assigned_programs: bool = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/programs",
            params={
                "assignedPrograms": assigned_programs,
                "sort": sort,
            },
            *args,
            **kwargs,
        )
