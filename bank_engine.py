from user_class import User

class Bank:
    def __init__(self):
        self.users = []
        self.accounts = []

    def reg_user(self, name, mail, password):
        user_id = (self.users) + 1
        new_user = User(user_id, name, mail, password)
        self.user.append(new_user)
        return new_user
    
    def auth_user(self, mail, password):
        for user in self.users:
            if user.mail == mail and User.authenticate(password):
                return user