from enum import Enum
from dataclasses import dataclass


class DoneeType(Enum):
    PROJECT = "PROJ"
    FUNDRAISER = "FUND"
    CART = "CART"
    CAMPAIGNER = "CAMP"
    MICROSITE = "MICS"


# create donor value object
@dataclass(frozen=True)
class Donee:
    ref_id: int
    name: str
    donee_type: DoneeType
    meta: dict
