class Account:
    def __init__(self, account_id, user_id, currency, balance=0):
        self.account_id = account_id
        self.user_id = user_id
        self.currency = currency
        self.balance = balance
        self.transaction_history = []
        self.limits = {
            "daily_withdrawal": None,
            "monthly_withdrawal": None,
            "daily_transfer": None,
            "monthly_transfer": None,
            "daily_spent": 0,
            "monthly_spent": 0,
            "last_reset_date": None,
        }
        
    def convert_currency(self, new_currency, exchange_rate):
        self.balance *= exchange_rate
        self.currency = new_currency