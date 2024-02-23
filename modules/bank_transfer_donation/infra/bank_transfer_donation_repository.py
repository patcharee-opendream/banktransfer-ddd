from modules.bank_transfer_donation.domain.aggregate.model import BankTransferDonation


class BankTransferDonationRepository:
    def __init__(self, session):
        self.session = session

    def create(self, bank_transfer_donation):
        self.session.add(bank_transfer_donation)
        # Note If not Id in bank_transfer_donation, PLS use flush() instead of commit() before return
        return bank_transfer_donation

    def get_by_id(self, id):
        return self.session.query(BankTransferDonation).get(id)

    def get_all(self):
        return self.session.query(BankTransferDonation).all()
