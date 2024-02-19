from dataclasses import dataclass
from datetime import datetime
from modules.note.domain.aggregate.id import NoteId

from modules.shared.domain.money import Money


@dataclass
class Note:
    id: NoteId
    note: str
    amount: Money
    date: datetime

    def new_note(note: str, amount: Money, date: datetime) -> "Note":
        return Note(
            id=NoteId.next_id(),
            note=note,
            amount=amount,
            date=date,
        )
