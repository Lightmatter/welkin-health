from welkin.models.base import Collection, Resource
from welkin.pagination import PageIterator
from welkin.util import model_id


class ProgramPhase(Resource):
    @model_id("Patient")
    def update(self, patient_id: str, program_name: str = None, **kwargs):
        program_name = program_name or self._parent.name
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/programs/"
            f"{program_name or self._parent.name}/phases",
            kwargs,
        )


class Program(Resource):
    subresources = [ProgramPhase]

    @model_id("Patient")
    def delete(self, patient_id: str):
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/programs/{self.name}"
        )

    @model_id("Patient")
    def update(self, patient_id: str, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/programs/{self.name}",
            kwargs,
        )


class Programs(Collection):
    resource = Program
    iterator = PageIterator

    @model_id("Patient")
    def get(
        self,
        patient_id: str,
        assigned_programs: bool = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
        params = {
            "assignedPrograms": assigned_programs,
            "sort": sort,
        }

        path = f"{self._client.instance}/patients/{patient_id}/programs"
        if hasattr(self, "programName"):
            path = f"{path}/current/{self.programName}"
        elif hasattr(self, "id"):
            path = f"{path}/history/{self.id}"
        else:
            raise AttributeError

        return super().get(
            path,
            params=params,
            *args,
            **kwargs,
        )
