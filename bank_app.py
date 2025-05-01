import customtkinter as ctk
from tkinter import messagebox


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
        self.current_user = None

        self.container = ctk.CTkFrame(self.app, fg_color="#FFFFF1")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.register_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")
        self.login_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")
        self.main_menu_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")

        self._create_register_frame()
        self._create_login_frame()
        self._create_main_menu_frame()

        self._show_frame("register")

        self.app.mainloop()

    def _show_frame(self, page_name):
        """Переключение между фреймами"""
        self.register_frame.grid_forget()
        self.login_frame.grid_forget()
        self.main_menu_frame.grid_forget()

        if page_name == "register":
            self.register_frame.grid(row=0, column=0, sticky="nsew")
        elif page_name == "login":
            self.login_frame.grid(row=0, column=0, sticky="nsew")
        elif page_name == "main":
            self.main_menu_frame.grid(row=0, column=0, sticky="nsew")

    def _create_register_frame(self):
        """Фрейм регистрации"""
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

        ctk.CTkButton(
            center_frame,
            text="Зарегистрироваться",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self._register_user,
        ).pack(pady=20, fill="x")

        ctk.CTkLabel(center_frame, text="Уже есть аккаунт?", font=self.font_style).pack(
            pady=5
        )
        ctk.CTkButton(
            center_frame,
            text="Войти",
            font=self.font_style,
            fg_color="gray",
            hover_color="darkgray",
            command=lambda: self._show_frame("login"),
        ).pack(pady=5, fill="x")

    def _create_login_frame(self):
        """Фрейм входа"""
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

        ctk.CTkButton(
            center_frame,
            text="Войти",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=self._login_user,
        ).pack(pady=20, fill="x")

        ctk.CTkLabel(center_frame, text="Нет аккаунта?", font=self.font_style).pack(
            pady=5
        )
        ctk.CTkButton(
            center_frame,
            text="Зарегистрироваться",
            font=self.font_style,
            fg_color="gray",
            hover_color="darkgray",
            command=lambda: self._show_frame("register"),
        ).pack(pady=5, fill="x")

    def _create_main_menu_frame(self):
        """Главное меню"""
        center_frame = ctk.CTkFrame(self.main_menu_frame, fg_color="#FFFFF1")
        center_frame.pack(expand=True, fill="both", padx=50, pady=20)

        label = ctk.CTkLabel(center_frame, text="Главное меню", font=self.title_font)
        label.pack(pady=(0, 20))

        operations = [
            ("Создать счет", self._create_account),
            ("Пополнить счет", self._deposit),
            ("Снять средства", self._withdraw),
            ("Перевести средства", self._transfer),
            ("Просмотреть баланс", self._get_balance),
        ]

        for text, command in operations:
            ctk.CTkButton(
                center_frame,
                text=text,
                font=self.font_style,
                fg_color=self.button_color,
                hover_color=self.button_hover_color,
                command=command,
            ).pack(pady=5, fill="x")

        ctk.CTkButton(
            center_frame,
            text="Выйти",
            font=self.font_style,
            fg_color="gray",
            hover_color="darkgray",
            command=self._logout,
        ).pack(pady=20, fill="x")

    def _register_user(self):
        """Регистрация пользователя"""
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()

        if not all([name, email, password]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if email in self.users:
            messagebox.showerror(
                "Ошибка", "Пользователь с такой почтой уже существует!"
            )
            return

        self.users[email] = {"name": name, "password": password, "accounts": []}

        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        self._clear_register_fields()
        self._show_frame("login")

    def _login_user(self):
        """Авторизация пользователя"""
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()

        if not all([email, password]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if email not in self.users:
            messagebox.showerror("Ошибка", "Пользователь не найден!")
            return

        if self.users[email]["password"] != password:
            messagebox.showerror("Ошибка", "Неверный пароль!")
            return

        self.current_user = email
        messagebox.showinfo("Успех", f"Добро пожаловать, {self.users[email]['name']}!")
        self._clear_login_fields()
        self._show_frame("main")

    def _create_account(self):
        """Создание счета"""
        if not self.current_user:
            messagebox.showerror("Ошибка", "Необходимо авторизоваться!")
            return

        account_id = f"ACC-{len(self.users[self.current_user]['accounts']) + 1:04d}"
        self.users[self.current_user]["accounts"].append(
            {"id": account_id, "balance": 0.0}
        )

        messagebox.showinfo("Успех", f"Счет {account_id} успешно создан!")

    def _deposit(self):
        """Пополнение счета"""
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для пополнения:")
        if not account_id:
            return

        amount = self._get_amount("Введите сумму для пополнения:")
        if amount is None:
            return

        for account in self.users[self.current_user]["accounts"]:
            if account["id"] == account_id:
                account["balance"] += amount
                messagebox.showinfo(
                    "Успех", f"Счет {account_id} пополнен на {amount} руб."
                )
                return

        messagebox.showerror("Ошибка", "Счет не найден!")

    def _withdraw(self):
        """Снятие средств"""
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для снятия:")
        if not account_id:
            return

        amount = self._get_amount("Введите сумму для снятия:")
        if amount is None:
            return
        for account in self.users[self.current_user]["accounts"]:
            if account["id"] == account_id:
                if account["balance"] >= amount:
                    account["balance"] -= amount
                    messagebox.showinfo(
                        "Успех", f"Со счета {account_id} снято {amount} руб."
                    )
                else:
                    messagebox.showerror("Ошибка", "Недостаточно средств!")
                return

        messagebox.showerror("Ошибка", "Счет не найден!")

    def _transfer(self):
        """Перевод средств"""
        if not self._check_auth():
            return

        from_account = self._get_account_id("Введите ID вашего счета:")
        if not from_account:
            return

        to_account = self._get_account_id("Введите ID счета получателя:")
        if not to_account:
            return

        amount = self._get_amount("Введите сумму для перевода:")
        if amount is None:
            return

        sender_account = None
        for account in self.users[self.current_user]["accounts"]:
            if account["id"] == from_account:
                sender_account = account
                break

        if not sender_account:
            messagebox.showerror("Ошибка", "Ваш счет не найден!")
            return

        if sender_account["balance"] < amount:
            messagebox.showerror("Ошибка", "Недостаточно средств!")
            return

        recipient_found = False
        for user in self.users.values():
            for account in user["accounts"]:
                if account["id"] == to_account:
                    account["balance"] += amount
                    sender_account["balance"] -= amount
                    messagebox.showinfo(
                        "Успех", f"Перевод {amount} руб. на счет {to_account} выполнен!"
                    )
                    return

        messagebox.showerror("Ошибка", "Счет получателя не найден!")

    def _get_balance(self):
        """Просмотр баланса"""
        if not self._check_auth():
            return

        accounts = self.users[self.current_user]["accounts"]
        if not accounts:
            messagebox.showinfo("Информация", "У вас нет открытых счетов")
            return

        balance_info = "\n".join(
            [f"Счет {acc['id']}: {acc['balance']:.2f} руб." for acc in accounts]
        )
        messagebox.showinfo("Ваши счета", balance_info)

    def _logout(self):
        """Выход из системы"""
        self.current_user = None
        self._show_frame("login")

    def _check_auth(self):
        """Проверка авторизации"""
        if not self.current_user:
            messagebox.showerror("Ошибка", "Необходимо авторизоваться!")
            return False
        return True

    def _get_account_id(self, prompt):
        """Получение ID счета"""
        dialog = ctk.CTkInputDialog(text=prompt, title="Ввод данных")
        return dialog.get_input()

    def _get_amount(self, prompt):
        """Получение суммы"""
        dialog = ctk.CTkInputDialog(text=prompt, title="Ввод суммы")
        try:
            return float(dialog.get_input())
        except (ValueError, TypeError):
            messagebox.showerror("Ошибка", "Введите корректную сумму!")
            return None

    def _clear_register_fields(self):
        """Очистка полей регистрации"""
        self.reg_name.delete(0, "end")
        self.reg_email.delete(0, "end")
        self.reg_password.delete(0, "end")

    def _clear_login_fields(self):
        """Очистка полей входа"""
        self.login_email.delete(0, "end")
        self.login_password.delete(0, "end")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    BankingApp()
