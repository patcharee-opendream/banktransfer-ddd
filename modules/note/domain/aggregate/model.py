from dataclasses import dataclass
from datetime import datetime

from modules.shared.domain.money import Money


@dataclass
class Note:
    note: str
    amount: Money
    date: datetime
