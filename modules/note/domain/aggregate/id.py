from pydantic import PositiveInt
from core.snowflake import seq


class NoteId(PositiveInt):
    gt = 1

    @staticmethod
    def next_id() -> "NoteId":
        return seq.__next__()
