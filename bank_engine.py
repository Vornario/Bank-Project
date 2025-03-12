
from user_class import User
from account_class import Account
from transaction_class import Transaction
from user_class import User
from error_handler_class import ErrorHandler

class Bank:
    def __init__(self):
        self.users = []
        self.accounts = []
        self.transactions = []
        self.error_handler = ErrorHandler()

    def reg_user(self, name, mail, password):
        user_id = len(self.users) + 1
        new_user = User(user_id, name, mail, password)
        self.users.append(new_user)
        return new_user

    def auth_user(self, mail, password):
        for user in self.users:
            if user.email == mail and user.authenticate(password):
                return user
        self.error_handler.add_error("Ошибка аутентификации: неверный логин или пароль")
        return None

    def create_account(self, user_id, currency_code):
        user = next((user for user in self.users if user.user_id == user_id), None)
        if not user:
            self.error_handler.add_error("Ошибка: пользователь не найден")
            return None
        account_id = len(self.accounts) + 1
        new_account = Account(account_id, user_id, currency_code)
        self.accounts.append(new_account)
        user.accounts.append(new_account)
        return new_account

    def deposit(self, account_id, amount):
        account = next((acc for acc in self.accounts if acc.account_id == account_id), None)
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return False
        account.balance += amount
        transaction = Transaction(len(self.transactions) + 1, None, account_id, amount, "deposit")
        self.transactions.append(transaction)
        account.transaction_history.append(transaction)
        return True

    def withdraw(self, account_id, amount):
        account = next((acc for acc in self.accounts if acc.account_id == account_id), None)
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return False
        if account.balance < amount:
            self.error_handler.add_error("Ошибка: недостаточно средств на счете")
            return False
        account.balance -= amount
        transaction = Transaction(len(self.transactions) + 1, account_id, None, amount, "withdraw")
        self.transactions.append(transaction)
        account.transaction_history.append(transaction)
        return True

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = next((acc for acc in self.accounts if acc.account_id == from_account_id), None)
        to_account = next((acc for acc in self.accounts if acc.account_id == to_account_id), None)
        if not from_account or not to_account:
            self.error_handler.add_error("Ошибка: один из счетов не найден")
            return False
        if from_account.balance < amount:
            self.error_handler.add_error("Ошибка: недостаточно средств на счете отправителя")
            return False
        from_account.balance -= amount
        to_account.balance += amount
        transaction = Transaction(len(self.transactions) + 1, from_account_id, to_account_id, amount, "transfer")
        self.transactions.append(transaction)
        from_account.transaction_history.append(transaction)
        to_account.transaction_history.append(transaction)
        return True

    def get_balance(self, account_id):
        account = next((acc for acc in self.accounts if acc.account_id == account_id), None)
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return None
        return account.balance

    def get_transaction_history(self, account_id):
        account = next((acc for acc in self.accounts if acc.account_id == account_id), None)
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return None
        return account.transaction_history