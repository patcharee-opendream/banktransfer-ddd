import pytest
from dataclasses import FrozenInstanceError

from modules.donor.domain.value_objects import Donor, DonorType


@pytest.fixture
def my_donor():
    return Donor(
        donor_type=DonorType.DONOR_TYPE_INDIVIDUAL,
        member_id="123",
        email="test@gmail.com",
        phone="1234567890",
        name1="John",
        name2="Doe",
        name_prefix="Mr.",
        tax_id="123456789",
    )


def test_donor(my_donor):
    donor_1 = my_donor
    donor_2 = Donor(
        donor_type=DonorType.DONOR_TYPE_INDIVIDUAL,
        member_id="123",
        email="test@gmail.com",
        phone="1234567890",
        name1="John",
        name2="Doe",
        name_prefix="Mr.",
        tax_id="123456789",
    )

    assert donor_1 == donor_2


def test_immutable_donor(my_donor):
    donor_1 = my_donor

    with pytest.raises(FrozenInstanceError):
        donor_1.member_id = "456"


def test_change_donor_name(my_donor):
    donor_1 = my_donor

    new_donor = donor_1.change_name(name1="Jane", name2="Doe")
    assert new_donor.name1 == "Jane"
    assert new_donor.name2 == "Doe"
