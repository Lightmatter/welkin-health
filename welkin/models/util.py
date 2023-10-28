from sys import modules


def find_patient_id_in_parents(model_instance):
    if isinstance(
        model_instance,
        getattr(modules["welkin.models"], "Patient"),
    ):
        return model_instance.id
    elif hasattr(model_instance, "patientId"):
        return model_instance.patientId
    elif model_instance._parent is not None:
        return find_patient_id_in_parents(model_instance._parent)
    else:
        raise Exception(
            f"Cannot find patient id. Model._parent chain ends in {model_instance}"
        )


class EncounterSubResource:
    """Utility class for subresources of Encounters to get patient and encounter ids"""

    @property
    def patient_id(self):
        if isinstance(
            self._parent._parent,
            getattr(modules["welkin.models"], "Patient"),
        ):
            return self._parent._parent.id

        if hasattr(self._parent, "patientId"):
            return self._parent.patientId

        # this is the related_data = True case on encounters
        return self._parent.encounter.patientId

    def get_patient_encounter_id(self, patient_id, encounter_id):
        """Helper to retrieve the necessary patient and encounter Ids"""
        if not patient_id:
            patient_id = self.patient_id

        if not encounter_id:
            encounter_id = self._parent.id

        return patient_id, encounter_id


def patient_id(func):
    """Wrapper for getting the patient id on patient subresources"""

    def wrapper(cls, *args, **kwargs):
        if "patient_id" not in kwargs:
            try:
                kwargs["patient_id"] = cls._parent.id
            except AttributeError:
                raise TypeError(
                    f"{func.__name__} is missing 1 required positional argument: "
                    "'patient_id"
                ) from None

        return func(cls, *args, **kwargs)

    return wrapper
