from enum import Enum
from modules.bank_transfer_donation.domain.aggregate.id import (
    BankTransferDonationId,
    BankTransferTransactionId,
)
from modules.donee.domain.value_objects import Donee
from dataclasses import dataclass
from modules.donor.domain.value_objects import Donor
from modules.note.domain.aggregate.model import Note
from modules.shared.domain.money import Money
from datetime import datetime


class BankTransferStatus(Enum):
    NEW = "new"
    PENDING = "pending"
    PAID = "paid"


@dataclass
class BankTransferTransaction:
    id: BankTransferTransactionId
    transaction_id: str
    date: datetime
    amount: Money
    note_id: int

    @staticmethod
    def new_transaction(
        transaction_id: str, date: datetime, amount: Money, note_id: int
    ) -> "BankTransferTransaction":
        transaction = BankTransferTransaction(
            id=BankTransferTransactionId.next_id(),
            transaction_id=transaction_id,
            date=date,
            amount=amount,
            note_id=note_id,
        )
        return transaction


@dataclass
class BankTransferDonation:
    id: BankTransferDonationId
    donation_number: str
    donor: Donor
    donee: Donee
    expected_amount: Money
    notes: list[Note]
    transactions: list[BankTransferTransaction]
    status: BankTransferStatus
    form_data: dict
    meta: dict

    @staticmethod
    def new_donation(
        donation_number: str,
        donor: Donor,
        donee: Donee,
        expected_amount: Money,
    ) -> "BankTransferDonation":
        donation = BankTransferDonation(
            id=BankTransferDonationId.next_id(),
            donation_number=donation_number,
            donor=donor,
            donee=donee,
            expected_amount=expected_amount,
            notes=[],
            transactions=[],
            status=BankTransferStatus.NEW,
            form_data={},
            meta={},
        )
        return donation

    def add_note(self, note, amount, date):
        if amount == 0:
            raise ValueError("Amount must be greater than 0")

        if not self.transactions:
            note = Note.new_note(
                note=note,
                amount=amount,
                date=date,
            )
            self.notes.append(note)
            self.status = BankTransferStatus.PENDING
        else:
            raise ValueError("Transaction already exists")

    def validate_note_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return True
        return False

    def confirm_transaction(
        self, transaction_id: str, date: datetime, amount: Money, note_id: int
    ):
        if not self.validate_note_id(note_id):
            raise ValueError("Note id does not exist")

        # create transaction
        transaction = BankTransferTransaction.new_transaction(
            transaction_id=transaction_id,
            date=date,
            amount=amount,
            note_id=note_id,
        )

        # append transaction to transactions list
        self.transactions.append(transaction)
        self.status = BankTransferStatus.PAID
