class Account:
    def __init__(self, account_id, user_id, currency, balance=0):
        self.account_id = account_id
        self.user_id = user_id
        self.currency = currency
        self.balance = balance
        self.transaction_history = []
