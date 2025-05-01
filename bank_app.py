import customtkinter as ctk
from tkinter import messagebox
from bank_engine import Bank


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


bank = Bank()
current_user = None


def register_user():
    name = entry_name.get()
    mail = entry_mail.get()
    password = entry_password.get()
    if name and mail and password:
        bank.reg_user(name, mail, password)
        messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован!")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля!")


def authenticate_user():
    global current_user
    mail = entry_auth_mail.get()
    password = entry_auth_password.get()
    if mail and password:
        user = bank.auth_user(mail, password)
        if user:
            current_user = user
            messagebox.showinfo("Успех", f"Добро пожаловать, {user.name}!")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля!")


def create_account():
    if current_user:
        account = bank.create_account(current_user.user_id, "RUB")
        if account:
            messagebox.showinfo("Успех", f"Счет {account.account_id} создан!")
        else:
            messagebox.showerror("Ошибка", "Не удалось создать счет!")
    else:
        messagebox.showerror("Ошибка", "Пользователь не авторизован!")


def deposit():
    account_id = get_account_id()
    amount = get_amount("Введите сумму для пополнения:")
    if account_id and amount:
        if bank.deposit(account_id, amount):
            messagebox.showinfo("Успех", "Счет успешно пополнен!")
        else:
            messagebox.showerror("Ошибка", "Не удалось пополнить счет!")


def withdraw():
    account_id = get_account_id()
    amount = get_amount("Введите сумму для снятия:")
    if account_id and amount:
        if bank.withdraw(account_id, amount):
            messagebox.showinfo("Успех", "Средства успешно сняты!")
        else:
            messagebox.showerror("Ошибка", "Не удалось снять средства!")


def transfer():
    from_account_id = get_account_id("Введите ID счета отправителя:")
    to_account_id = get_account_id("Введите ID счета получателя:")
    amount = get_amount("Введите сумму для перевода:")
    if from_account_id and to_account_id and amount:
        if bank.transfer(from_account_id, to_account_id, amount):
            messagebox.showinfo("Успех", "Перевод выполнен успешно!")
        else:
            messagebox.showerror("Ошибка", "Не удалось выполнить перевод!")


def get_balance():
    account_id = get_account_id()
    if account_id:
        balance = bank.get_balance(account_id)
        if balance is not None:
            messagebox.showinfo("Баланс", f"Ваш баланс: {balance}")
        else:
            messagebox.showerror("Ошибка", "Не удалось получить баланс!")


def get_account_id(prompt="Введите ID счета:"):
    return get_input(prompt)


def get_amount(prompt):
    return get_input(prompt, is_numeric=True)


def get_input(prompt, is_numeric=False):
    dialog = ctk.CTkInputDialog(text=prompt, title="Ввод данных")
    user_input = dialog.get_input()
    if user_input:
        if is_numeric:
            try:
                return float(user_input)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите число!")
                return None
        return user_input
    return None


import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class BankingApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Банковская система")
        self.app.geometry("400x700")
        self.app.configure(fg_color="#FFFFF1")

        self.font_style = ("Georgia", 14)
        self.title_font = ("Georgia", 16, "bold")
        self.button_color = "#8B8B83"
        self.button_hover_color = "#6B6B63"

        self.users = {}

        self.container = ctk.CTkFrame(self.app, fg_color="#FFFFF1")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.register_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")
        self.login_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")
        self.main_menu_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")

        self.create_register_frame()
        self.create_login_frame()
        self.create_main_menu_frame()

        self.show_frame("register")

        self.app.mainloop()

    def show_frame(self, page_name):
        """Показывает указанный фрейм"""
        self.register_frame.grid_forget()
        self.login_frame.grid_forget()
        self.main_menu_frame.grid_forget()

        if page_name == "register":
            self.register_frame.grid(row=0, column=0, sticky="nsew")
        elif page_name == "login":
            self.login_frame.grid(row=0, column=0, sticky="nsew")
        elif page_name == "main":
            self.main_menu_frame.grid(row=0, column=0, sticky="nsew")

    def create_register_frame(self):
        """Создает фрейм регистрации"""
        center_frame = ctk.CTkFrame(self.register_frame, fg_color="#FFFFF1")
        center_frame.pack(expand=True, fill="both", padx=50, pady=20)

        label = ctk.CTkLabel(center_frame, text="Регистрация", font=self.title_font)
        label.pack(pady=(0, 20))

        self.reg_name = ctk.CTkEntry(
            center_frame, placeholder_text="Имя", font=self.font_style
        )
        self.reg_name.pack(pady=5, fill="x")

        self.reg_email = ctk.CTkEntry(
            center_frame, placeholder_text="Почта", font=self.font_style
        )
        self.reg_email.pack(pady=5, fill="x")

        self.reg_password = ctk.CTkEntry(
            center_frame, placeholder_text="Пароль", show="*", font=self.font_style
        )
        self.reg_password.pack(pady=5, fill="x")

        button_register = ctk.CTkButton(
            center_frame,
            text="Зарегистрироваться",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.register_user,
        )
        button_register.pack(pady=20, fill="x")

        label_have_account = ctk.CTkLabel(
            center_frame, text="Уже есть аккаунт?", font=self.font_style
        )
        label_have_account.pack(pady=5)

        button_to_login = ctk.CTkButton(
            center_frame,
            text="Войти",
            font=self.font_style,
            fg_color="gray",
            hover_color="darkgray",
            command=lambda: self.show_frame("login"),
        )
        button_to_login.pack(pady=5, fill="x")

    def create_login_frame(self):
        """Создает фрейм входа"""
        center_frame = ctk.CTkFrame(self.login_frame, fg_color="#FFFFF1")
        center_frame.pack(expand=True, fill="both", padx=50, pady=20)

        label = ctk.CTkLabel(center_frame, text="Вход в аккаунт", font=self.title_font)
        label.pack(pady=(0, 20))

        self.login_email = ctk.CTkEntry(
            center_frame, placeholder_text="Почта", font=self.font_style
        )
        self.login_email.pack(pady=5, fill="x")

        self.login_password = ctk.CTkEntry(
            center_frame, placeholder_text="Пароль", show="*", font=self.font_style
        )
        self.login_password.pack(pady=5, fill="x")

        button_login = ctk.CTkButton(
            center_frame,
            text="Войти",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.login_user,
        )
        button_login.pack(pady=20, fill="x")

        label_no_account = ctk.CTkLabel(
            center_frame, text="Нет аккаунта?", font=self.font_style
        )
        label_no_account.pack(pady=5)

        button_to_register = ctk.CTkButton(
            center_frame,
            text="Зарегистрироваться",
            font=self.font_style,
            fg_color="gray",
            hover_color="darkgray",
            command=lambda: self.show_frame("register"),
        )
        button_to_register.pack(pady=5, fill="x")

    def create_main_menu_frame(self):
        """Создает главное меню"""
        center_frame = ctk.CTkFrame(self.main_menu_frame, fg_color="#FFFFF1")
        center_frame.pack(expand=True, fill="both", padx=50, pady=20)

        label = ctk.CTkLabel(center_frame, text="Главное меню", font=self.title_font)
        label.pack(pady=(0, 20))

        button_create_account = ctk.CTkButton(
            center_frame,
            text="Создать счет",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.create_account,
        )
        button_create_account.pack(pady=5, fill="x")

        button_deposit = ctk.CTkButton(
            center_frame,
            text="Пополнить счет",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.deposit,
        )
        button_deposit.pack(pady=5, fill="x")

        button_withdraw = ctk.CTkButton(
            center_frame,
            text="Снять средства",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.withdraw,
        )
        button_withdraw.pack(pady=5, fill="x")

        button_transfer = ctk.CTkButton(
            center_frame,
            text="Перевести средства",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.transfer,
        )
        button_transfer.pack(pady=5, fill="x")

        button_balance = ctk.CTkButton(
            center_frame,
            text="Просмотреть баланс",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self.get_balance,
        )
        button_balance.pack(pady=5, fill="x")

        button_logout = ctk.CTkButton(
            center_frame,
            text="Выйти",
            font=self.font_style,
            fg_color="gray",
            hover_color="darkgray",
            command=lambda: self.show_frame("login"),
        )
        button_logout.pack(pady=20, fill="x")

    def register_user(self):
        """Регистрация нового пользователя"""
        name = self.reg_name.get()
        email = self.reg_email.get()
        password = self.reg_password.get()

        if not name or not email or not password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if email in self.users:
            messagebox.showerror(
                "Ошибка", "Пользователь с такой почтой уже существует!"
            )
            return

        self.users[email] = {"name": name, "password": password, "accounts": []}

        messagebox.showinfo(
            "Успех", "Регистрация прошла успешно! Теперь вы можете войти."
        )
        self.show_frame("login")
        self.reg_name.delete(0, "end")
        self.reg_email.delete(0, "end")
        self.reg_password.delete(0, "end")

    def login_user(self):
        """Вход пользователя"""
        email = self.login_email.get()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if email not in self.users:
            messagebox.showerror("Ошибка", "Пользователь с такой почтой не найден!")
            return

        if self.users[email]["password"] != password:
            messagebox.showerror("Ошибка", "Неверный пароль!")
            return

        self.current_user = email
        messagebox.showinfo("Успех", f"Добро пожаловать, {self.users[email]['name']}!")
        self.show_frame("main")
        self.login_email.delete(0, "end")
        self.login_password.delete(0, "end")

    def create_account(self):
        """Создание счета"""
        if not hasattr(self, "current_user"):
            return

        account_id = f"ACC-{len(self.users[self.current_user]['accounts']) + 1:04d}"
        self.users[self.current_user]["accounts"].append(
            {"id": account_id, "balance": 0}
        )

        messagebox.showinfo("Успех", f"Счет {account_id} успешно создан!")

    def deposit(self):
        """Пополнение счета"""
        if not hasattr(self, "current_user"):
            return

        messagebox.showinfo("Информация", "Функция пополнения счета в разработке")

    def withdraw(self):
        """Снятие средств"""
        if not hasattr(self, "current_user"):
            return

        messagebox.showinfo("Информация", "Функция снятия средств в разработке")

    def transfer(self):
        """Перевод средств"""
        if not hasattr(self, "current_user"):
            return

        messagebox.showinfo("Информация", "Функция перевода средств в разработке")

    def get_balance(self):
        """Просмотр баланса"""
        if not hasattr(self, "current_user"):
            return

        accounts = self.users[self.current_user]["accounts"]
        if not accounts:
            messagebox.showinfo("Баланс", "У вас нет открытых счетов")
            return

        balance_info = "\n".join(
            [f"Счет {acc['id']}: {acc['balance']} руб." for acc in accounts]
        )
        messagebox.showinfo("Ваши счета", balance_info)


if __name__ == "__main__":
    BankingApp()
