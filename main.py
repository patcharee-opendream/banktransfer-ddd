from decimal import Decimal
from fastapi import Depends, FastAPI
from pytest import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.bank_transfer_donation.domain.aggregate.model import (
    BankTransferDonation,
)
from modules.bank_transfer_donation.infra.bank_transfer_donation_repository import (
    BankTransferDonationRepository,
)
from modules.bank_transfer_donation.infra.mapper import metadata
from modules.bank_transfer_donation.infra.mapper import start_mapper
import asyncio

from modules.donee.domain.value_objects import Donee
from modules.donor.domain.value_objects import Donor


# start to connect to the database
def get_db():
    print("Connecting to the database...")
    start_mapper()

    DATABASE_URL = "postgresql://toy:1234@localhost:5432/test"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata.create_all(engine)
    return session, engine


app = FastAPI()
session, engine = get_db()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down")
    session.close()
    engine.dispose()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/bank-transfer-donations/")
def read_bank_transfer_donations():
    repo = BankTransferDonationRepository(session)
    donations = repo.get_all()
    return donations


@app.get("/bank-transfer-donations-async/")
async def read_bank_transfer_donations():
    repo = BankTransferDonationRepository(session)
    donations = await asyncio.to_thread(repo.get_all)
    return donations


@app.post("/bank-transfer-donation/")
def create_bank_transfer_donation(
    donation_number: str,
    donor: Donor,
    donee: Donee,
):

    print("Creating a new bank transfer donation...")

    # create a new bank transfer donation
    donation = BankTransferDonation.new_donation(
        donation_number=donation_number,
        donor=donor,
        donee=donee,
        expected_amount=None,
    )
    print("donation", donation)
    repo = BankTransferDonationRepository(session)

    created_donation = repo.create(donation)
    session.commit()

    return created_donation
