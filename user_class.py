class User:
    def __init__(self, user_id, name, email, password, accounts):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.accounts = accounts

    def add_account(self, account):
        self.accounts.append(account)

    def authenticate(self, password):
        return self.password == password #test
