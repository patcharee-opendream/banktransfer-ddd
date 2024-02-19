from datetime import datetime
import pytest
from modules.bank_transfer_donation.domain.aggregate.model import (
    BankTransferDonation,
    BankTransferStatus,
)
from modules.donee.domain.value_objects import Donee, DoneeType

from modules.donor.domain.value_objects import Donor, DonorType
from modules.shared.domain.money import Money


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


def test_add_notes_to_bank_transfer_donation(my_donor):
    donee = Donee(
        donee_type=DoneeType.PROJECT,
        ref_id="123",
        name="test",
        meta={},
    )

    donation = BankTransferDonation(
        id=1,
        donation_number="123",
        donor=my_donor,
        donee=donee,
        expected_amount=None,
    )

    assert donation.notes == []
    assert donation.status == BankTransferStatus.NEW
    assert donation.transactions == []
    assert donation.form_data == {}
    assert donation.meta == {}

    donation.add_note("test", Money(amount=100, currency="USD"), datetime.now())
    assert donation.status == BankTransferStatus.PENDING
    assert len(donation.notes) == 1


def test_approve_bank_transfer_donation():
    pass
