from enum import Enum
from modules.donee.domain.value_objects import Donee

from modules.donor.domain.value_objects import Donor
from modules.note.domain.aggregate.model import Note
from modules.shared.domain.money import Money


class BankTransferStatus(Enum):
    NEW = "new"
    PENDING = "pending"
    PAID = "paid"


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
        self.transactions = []
        self.status = BankTransferStatus.NEW
        self.form_data = {}
        self.meta = {}

    def add_note(self, note, amount, date):
        if amount == 0:
            raise ValueError("Amount must be greater than 0")

        if not self.transactions:
            note = Note(
                note=note,
                amount=amount,
                date=date,
            )
            self.notes.append(note)
            self.status = BankTransferStatus.PENDING
        else:
            raise ValueError("Transaction already exists")
