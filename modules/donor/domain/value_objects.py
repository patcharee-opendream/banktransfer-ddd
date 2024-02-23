from enum import Enum
from dataclasses import dataclass


class DonorType(Enum):
    PER = "PER"
    ORG = "ORG"

    def __composite_values__(self):
        return (self.value,)


# create donor value object
@dataclass(frozen=True)
class Donor:
    donor_type: DonorType
    member_id: str
    email: str
    phone: str
    name1: str
    name2: str
    name_prefix: str
    tax_id: str

    def change_name(self, name1: str, name2: str) -> "Donor":
        return Donor(
            donor_type=self.donor_type,
            member_id=self.member_id,
            email=self.email,
            phone=self.phone,
            name1=name1,
            name2=name2,
            name_prefix=self.name_prefix,
            tax_id=self.tax_id,
        )
