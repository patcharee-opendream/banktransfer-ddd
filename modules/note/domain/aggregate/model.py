from dataclasses import dataclass
from datetime import datetime

from modules.shared.domain.money import Money


class Note:
    def __init__(self, id: int, note: str, amount: Money, date: datetime):
        self.id = id
        self.note = note
        self.amount = amount
        self.date = date
