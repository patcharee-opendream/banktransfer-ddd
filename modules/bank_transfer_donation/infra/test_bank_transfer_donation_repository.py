from modules.bank_transfer_donation.domain.aggregate.model import BankTransferDonation
from modules.bank_transfer_donation.infra.bank_transfer_donation_repository import (
    BankTransferDonationRepository,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from modules.bank_transfer_donation.infra.mapper import start_mapper
from modules.donee.domain.value_objects import Donee, DoneeType
from modules.donor.domain.value_objects import Donor, DonorType
from modules.bank_transfer_donation.infra.mapper import metadata


@pytest.fixture
def my_donor():
    return Donor(
        donor_type=DonorType.PER,
        member_id="123",
        email="test@gmail.com",
        phone="1234567890",
        name1="John",
        name2="Doe",
        name_prefix="Mr.",
        tax_id="123456789",
    )


@pytest.fixture
def session():
    start_mapper()

    DATABASE_URL = "postgresql://toy:1234@localhost:5432/test"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata.create_all(engine)
    return session


def test_get_all_bank_transfer_donation_repository(session, my_donor):
    donee = Donee(
        donee_type=DoneeType.PROJ,
        ref_id="123",
        name="test",
        meta={},
    )

    donation = BankTransferDonation.new_donation(
        donation_number="123",
        donor=my_donor,
        donee=donee,
        expected_amount=None,
    )

    # Create a repository
    repo = BankTransferDonationRepository(session)

    all = repo.get_all()
    assert len(all) == 0

    created_donation = repo.create(donation)
    session.flush()

    donations = repo.get_all()
    assert created_donation == donation
    assert len(donations) == 1

    session.rollback()
