from datetime import datetime


class Transaction:
    def __init__(
        self,
        transaction_id,
        account_from,
        account_to,
        amount,
        transaction_type,
        date=None,
    ):
        self.transaction_id = transaction_id
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = date if date is not None else datetime.now()
