from pydantic import PositiveInt
from core.snowflake import seq


class BankTransferTransactionId(PositiveInt):
    gt = 1

    @staticmethod
    def next_id() -> "BankTransferTransactionId":
        return seq.__next__()


class BankTransferDonationId(PositiveInt):
    gt = 1

    @staticmethod
    def next_id() -> "BankTransferDonationId":
        return seq.__next__()
