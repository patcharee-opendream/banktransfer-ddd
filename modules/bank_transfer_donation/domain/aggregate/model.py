from enum import Enum
from modules.donee.domain.value_objects import Donee

from modules.donor.domain.value_objects import Donor
from modules.note.domain.aggregate.model import Note
from modules.shared.domain.money import Money
from datetime import datetime


class BankTransferStatus(Enum):
    NEW = "new"
    PENDING = "pending"
    PAID = "paid"


class BankTransferTransaction:
    def __init__(
        self,
        id: int,
        transaction_id: str,
        date: datetime,
        amount: Money,
        note_id: int,
    ):
        self.id = id
        self.transaction_id = transaction_id
        self.date = date
        self.amount = amount
        self.note_id = note_id


class BankTransferDonation:
    def __init__(
        self,
        id: int,
        donation_number: str,
        donor: Donor,
        donee: Donee,
        expected_amount: Money,
    ):
        self.id = id
        self.donation_number = donation_number
        self.donor = donor
        self.donee = donee
        self.expected_amount = expected_amount

        self.notes = []
        self.transactions: list[BankTransferTransaction] = []
        self.status = BankTransferStatus.NEW
        self.form_data = {}
        self.meta = {}

    def add_note(self, note, amount, date):
        if amount == 0:
            raise ValueError("Amount must be greater than 0")

        if not self.transactions:
            note = Note(
                id=1,
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
        transaction = BankTransferTransaction(
            id=1,
            transaction_id=transaction_id,
            date=date,
            amount=amount,
            note_id=note_id,
        )

        # append transaction to transactions list
        self.transactions.append(transaction)
        self.status = BankTransferStatus.PAID
