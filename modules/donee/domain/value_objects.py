from enum import Enum
from dataclasses import dataclass


class DoneeType(Enum):
    PROJ = "PROJ"
    FUND = "FUND"
    CART = "CART"
    CAMP = "CAMP"
    MICS = "MICS"


# create donor value object
@dataclass(frozen=True)
class Donee:
    ref_id: int
    name: str
    donee_type: DoneeType
    meta: dict
