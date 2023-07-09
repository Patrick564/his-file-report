from typing import NamedTuple


class Patient(NamedTuple):
    hlc: str
    district: str
    establishment: str
    sector: str
    insurance: int
    father_last_name: str
    mother_last_name: str
    names: str
    gender: int
    birthday: str
    appointment: str
    type_of_birth: int


Patients = dict[str, Patient]
