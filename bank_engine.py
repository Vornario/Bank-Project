from user_class import User
from account_class import Account
from transaction_class import Transaction
from user_class import User
from error_handler_class import ErrorHandler
from datetime import datetime


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
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return False
        account.balance += amount
        transaction = Transaction(
            len(self.transactions) + 1, None, account_id, amount, "deposit"
        )
        self.transactions.append(transaction)
        account.transaction_history.append(transaction)
        return True

    def withdraw(self, account_id, amount):
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return False
        if account.balance < amount:
            self.error_handler.add_error("Ошибка: недостаточно средств на счете")
            return False
        account.balance -= amount
        transaction = Transaction(
            len(self.transactions) + 1, account_id, None, amount, "withdraw"
        )
        self.transactions.append(transaction)
        account.transaction_history.append(transaction)
        return True

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = next(
            (acc for acc in self.accounts if acc.account_id == from_account_id), None
        )
        to_account = next(
            (acc for acc in self.accounts if acc.account_id == to_account_id), None
        )
        if not from_account or not to_account:
            self.error_handler.add_error("Ошибка: один из счетов не найден")
            return False
        if from_account.balance < amount:
            self.error_handler.add_error(
                "Ошибка: недостаточно средств на счете отправителя"
            )
            return False
        from_account.balance -= amount
        to_account.balance += amount
        transaction = Transaction(
            len(self.transactions) + 1,
            from_account_id,
            to_account_id,
            amount,
            "transfer",
        )
        self.transactions.append(transaction)
        from_account.transaction_history.append(transaction)
        to_account.transaction_history.append(transaction)
        return True

    def get_balance(self, account_id):
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return None
        return account.balance

    def get_transaction_history(self, account_id):
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return None
        return account.transaction_history

    def set_limit(self, account_id, limit_type, amount):
        """Установка лимита для счета"""
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return False

        if limit_type not in [
            "daily_withdrawal",
            "monthly_withdrawal",
            "daily_transfer",
            "monthly_transfer",
        ]:
            self.error_handler.add_error("Ошибка: неверный тип лимита")
            return False

        account.limits[limit_type] = amount
        self._reset_spent_if_needed(account)
        return True

    def _reset_spent_if_needed(self, account):
        """Сброс счетчиков потраченных сумм при смене дня/месяца"""
        today = datetime.now().date()

        if account.limits["last_reset_date"] != today:
            if (
                account.limits["last_reset_date"] is None
                or account.limits["last_reset_date"].month != today.month
            ):
                account.limits["monthly_spent"] = 0
            account.limits["daily_spent"] = 0
            account.limits["last_reset_date"] = today

    def _check_limit(self, account, amount, operation_type):
        """Проверка лимитов перед операцией"""
        self._reset_spent_if_needed(account)

        if operation_type == "withdraw":
            daily_limit = account.limits["daily_withdrawal"]
            monthly_limit = account.limits["monthly_withdrawal"]
        elif operation_type == "transfer":
            daily_limit = account.limits["daily_transfer"]
            monthly_limit = account.limits["monthly_transfer"]
        else:
            return True

        if (
            daily_limit is not None
            and account.limits["daily_spent"] + amount > daily_limit
        ):
            self.error_handler.add_error(f"Превышен дневной лимит {operation_type}")
            return False

        if (
            monthly_limit is not None
            and account.limits["monthly_spent"] + amount > monthly_limit
        ):
            self.error_handler.add_error(f"Превышен месячный лимит {operation_type}")
            return False

        return True

    def withdraw(self, account_id, amount):
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return False

        if not self._check_limit(account, amount, "withdraw"):
            return False

        if account.balance < amount:
            self.error_handler.add_error("Ошибка: недостаточно средств на счете")
            return False

        account.balance -= amount
        account.limits["daily_spent"] += amount
        account.limits["monthly_spent"] += amount

        transaction = Transaction(
            len(self.transactions) + 1,
            account_id,
            None,
            amount,
            "withdraw",
            datetime.now(),
        )
        self.transactions.append(transaction)
        account.transaction_history.append(transaction)
        return True

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = next(
            (acc for acc in self.accounts if acc.account_id == from_account_id), None
        )
        to_account = next(
            (acc for acc in self.accounts if acc.account_id == to_account_id), None
        )
        if not from_account or not to_account:
            self.error_handler.add_error("Ошибка: один из счетов не найден")
            return False

        if not self._check_limit(from_account, amount, "transfer"):
            return False

        if from_account.balance < amount:
            self.error_handler.add_error(
                "Ошибка: недостаточно средств на счете отправителя"
            )
            return False

        from_account.balance -= amount
        to_account.balance += amount
        from_account.limits["daily_spent"] += amount
        from_account.limits["monthly_spent"] += amount

        transaction = Transaction(
            len(self.transactions) + 1,
            from_account_id,
            to_account_id,
            amount,
            "transfer",
            datetime.now(),
        )
        self.transactions.append(transaction)
        from_account.transaction_history.append(transaction)
        to_account.transaction_history.append(transaction)
        return True

    def get_limits(self, account_id):
        """Получение текущих лимитов счета"""
        account = next(
            (acc for acc in self.accounts if acc.account_id == account_id), None
        )
        if not account:
            self.error_handler.add_error("Ошибка: счет не найден")
            return None
        return account.limits
