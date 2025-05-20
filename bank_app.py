import customtkinter as ctk
from tkinter import messagebox
from bank_engine import Bank


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

        self.current_user = None
        self.bank = Bank()

        self.container = ctk.CTkFrame(self.app, fg_color="#FFFFF1")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.register_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")
        self.login_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")
        self.main_menu_frame = ctk.CTkFrame(self.container, fg_color="#FFFFF1")

        self.exchange_rates = {
            "RUB": {"USD": 0.011, "CNY": 0.079, "GBP": 0.0087, "EUR": 0.010},
            "USD": {"RUB": 90.0, "CNY": 7.2, "GBP": 0.79, "EUR": 0.92},
            "CNY": {"RUB": 12.6, "USD": 0.14, "GBP": 0.11, "EUR": 0.13},
            "GBP": {"RUB": 114.5, "USD": 1.27, "CNY": 9.1, "EUR": 1.17},
            "EUR": {"RUB": 98.0, "USD": 1.09, "CNY": 7.8, "GBP": 0.86},
        }

        self._create_register_frame()
        self._create_login_frame()
        self._create_main_menu_frame()

        self._show_frame("register")

        self.app.mainloop()

    def _show_frame(self, page_name):
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
            ("История операций", self._view_transaction_history),
            ("Изменить валюту счета", self._change_currency),
            ("Курсы валют", self._view_exchange_rates),
            ("Установить лимиты", self._set_limits),
            ("Просмотреть лимиты", self._view_limits),
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
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()

        if not all([name, email, password]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if any(user.email == email for user in self.bank.users):
            messagebox.showerror(
                "Ошибка", "Пользователь с такой почтой уже существует!"
            )
            return

        new_user = self.bank.reg_user(name, email, password)
        if new_user:
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self._clear_register_fields()
            self._show_frame("login")

    def _login_user(self):

        email = self.login_email.get().strip()
        password = self.login_password.get().strip()

        if not all([email, password]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        user = self.bank.auth_user(email, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Успех", f"Добро пожаловать, {user.name}!")
            self._clear_login_fields()
            self._show_frame("main")
        else:
            messagebox.showerror("Ошибка", "Неверный email или пароль!")

    def _create_account(self):
        if not self._check_auth():
            return

        currency_window = ctk.CTkToplevel(self.app)
        currency_window.title("Выбор валюты счета")
        currency_window.geometry("300x300")

        ctk.CTkLabel(
            currency_window,
            text="Выберите валюту счета:",
            font=self.title_font,
        ).pack(pady=10)

        currencies = ["RUB", "USD", "EUR", "GBP", "CNY"]
        self.account_currency_var = ctk.StringVar(value="RUB")

        for currency in currencies:
            ctk.CTkRadioButton(
                currency_window,
                text=currency,
                variable=self.account_currency_var,
                value=currency,
                font=self.font_style,
            ).pack(pady=2)

        ctk.CTkButton(
            currency_window,
            text="Создать счет",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=lambda: self._finish_account_creation(currency_window),
        ).pack(pady=20)

    def _finish_account_creation(self, window):
        currency = self.account_currency_var.get()
        account = self.bank.create_account(self.current_user.user_id, currency)
        window.destroy()

        if account:
            messagebox.showinfo(
                "Успех",
                f"Счет {account.account_id} в валюте {currency} успешно создан!",
            )
        else:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])

    def _deposit(self):
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для пополнения:")
        if not account_id:
            return

        try:
            account_id = int(account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        amount = self._get_amount("Введите сумму для пополнения:")
        if amount is None:
            return

        if self.bank.deposit(account_id, amount):
            messagebox.showinfo("Успех", f"Счет {account_id} пополнен на {amount} руб.")
        else:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])

    def _withdraw(self):
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для снятия:")
        if not account_id:
            return

        try:
            account_id = int(account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        amount = self._get_amount("Введите сумму для снятия:")
        if amount is None:
            return

        if self.bank.withdraw(account_id, amount):
            messagebox.showinfo("Успех", f"Со счета {account_id} снято {amount} руб.")
        else:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])

    def _transfer(self):
        if not self._check_auth():
            return

        from_account_id = self._get_account_id("Введите ID вашего счета:")
        if not from_account_id:
            return

        to_account_id = self._get_account_id("Введите ID счета получателя:")
        if not to_account_id:
            return

        try:
            from_account_id = int(from_account_id)
            to_account_id = int(to_account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        amount = self._get_amount("Введите сумму для перевода:")
        if amount is None:
            return

        # Получаем информацию о валютах счетов
        from_currency = self.bank.get_account_currency(from_account_id)
        to_currency = self.bank.get_account_currency(to_account_id)

        if from_currency is None or to_currency is None:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])
            return

        # Если валюты разные, показываем информацию о конвертации
        if from_currency != to_currency:
            exchange_rate = self.exchange_rates.get(from_currency, {}).get(to_currency)
            if exchange_rate is None:
                messagebox.showerror(
                    "Ошибка", "Невозможно выполнить перевод между этими валютами"
                )
                return

            converted_amount = amount * exchange_rate
            confirm = messagebox.askyesno(
                "Подтверждение перевода",
                f"Вы переводите {amount:.2f} {from_currency} на счет в {to_currency}\n"
                f"Курс обмена: 1 {from_currency} = {exchange_rate:.4f} {to_currency}\n"
                f"Получатель получит: {converted_amount:.2f} {to_currency}\n\n"
                "Продолжить перевод?",
            )
            if not confirm:
                return

        if self.bank.transfer(from_account_id, to_account_id, amount):
            message = f"Перевод {amount:.2f} {from_currency} на счет {to_account_id} выполнен!"
            if from_currency != to_currency:
                message += (
                    f"\nПолучателю зачислено: {converted_amount:.2f} {to_currency}"
                )
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])

    def _get_balance(self):
        if not self._check_auth():
            return

        accounts = [
            acc
            for acc in self.bank.accounts
            if acc.user_id == self.current_user.user_id
        ]
        if not accounts:
            messagebox.showinfo("Информация", "У вас нет открытых счетов")
            return

        balance_info = "\n".join(
            [
                f"Счет {acc.account_id}: {acc.balance:.2f} {acc.currency}"
                for acc in accounts
            ]
        )
        messagebox.showinfo("Ваши счета", balance_info)

    def _logout(self):
        self.current_user = None
        self._show_frame("login")

    def _check_auth(self):
        if not self.current_user:
            messagebox.showerror("Ошибка", "Необходимо авторизоваться!")
            return False
        return True

    def _get_account_id(self, prompt):
        dialog = ctk.CTkInputDialog(text=prompt, title="Ввод данных")
        return dialog.get_input()

    def _get_amount(self, prompt):
        dialog = ctk.CTkInputDialog(text=prompt, title="Ввод суммы")
        try:
            return float(dialog.get_input())
        except (ValueError, TypeError):
            messagebox.showerror("Ошибка", "Введите корректную сумму!")
            return None

    def _clear_register_fields(self):
        self.reg_name.delete(0, "end")
        self.reg_email.delete(0, "end")
        self.reg_password.delete(0, "end")

    def _clear_login_fields(self):
        self.login_email.delete(0, "end")
        self.login_password.delete(0, "end")

    def _set_limits(self):
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для установки лимитов:")
        if not account_id:
            return

        try:
            account_id = int(account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        account = next(
            (acc for acc in self.bank.accounts if acc.account_id == account_id), None
        )
        if not account or account.user_id != self.current_user.user_id:
            messagebox.showerror("Ошибка", "Счет не найден или не принадлежит вам!")
            return

        limit_window = ctk.CTkToplevel(self.app)
        limit_window.title("Установка лимитов")
        limit_window.geometry("400x400")

        ctk.CTkLabel(
            limit_window,
            text=f"Установка лимитов для счета {account_id}",
            font=self.title_font,
        ).pack(pady=10)

        limit_types = [
            ("daily_withdrawal", "Дневной лимит на снятие"),
            ("monthly_withdrawal", "Месячный лимит на снятие"),
            ("daily_transfer", "Дневной лимит на переводы"),
            ("monthly_transfer", "Месячный лимит на переводы"),
        ]

        self.limit_entries = {}

        for limit_type, label_text in limit_types:
            frame = ctk.CTkFrame(limit_window)
            frame.pack(pady=5, fill="x", padx=20)

            ctk.CTkLabel(frame, text=label_text + ":", width=150).pack(side="left")
            entry = ctk.CTkEntry(frame)
            entry.pack(side="right", expand=True, fill="x")
            self.limit_entries[limit_type] = entry

        ctk.CTkButton(
            limit_window,
            text="Установить лимиты",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=lambda: self._apply_limits(account_id, limit_window),
        ).pack(pady=20)

    def _apply_limits(self, account_id, window):
        try:
            for limit_type, entry in self.limit_entries.items():
                value = entry.get().strip()
                if value:
                    amount = float(value)
                    if not self.bank.set_limit(account_id, limit_type, amount):
                        messagebox.showerror(
                            "Ошибка", self.bank.error_handler.errors[-1]
                        )
                        return
                else:
                    self.bank.set_limit(account_id, limit_type, None)

            messagebox.showinfo("Успех", "Лимиты успешно установлены!")
            window.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму!")

    def _view_limits(self):
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для просмотра лимитов:")
        if not account_id:
            return

        try:
            account_id = int(account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        account = next(
            (acc for acc in self.bank.accounts if acc.account_id == account_id), None
        )
        if not account or account.user_id != self.current_user.user_id:
            messagebox.showerror("Ошибка", "Счет не найден или не принадлежит вам!")
            return

        limits = self.bank.get_limits(account_id)
        if limits is None:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])
            return

        limit_info = (
            f"Дневной лимит на снятие: {limits['daily_withdrawal'] or 'не установлен'}\n"
            f"Месячный лимит на снятие: {limits['monthly_withdrawal'] or 'не установлен'}\n"
            f"Дневной лимит на переводы: {limits['daily_transfer'] or 'не установлен'}\n"
            f"Месячный лимит на переводы: {limits['monthly_transfer'] or 'не установлен'}\n\n"
            f"Потрачено сегодня: {limits['daily_spent']:.2f} руб.\n"
            f"Потрачено в этом месяце: {limits['monthly_spent']:.2f} руб."
        )

        messagebox.showinfo(f"Лимиты счета {account_id}", limit_info)

    def _view_transaction_history(self):
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для просмотра истории:")
        if not account_id:
            return

        try:
            account_id = int(account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        history = self.bank.get_transaction_history(account_id)
        if history is None:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])
            return

        if not history:
            messagebox.showinfo("История операций", "По этому счету нет операций")
            return

        history_text = "История операций:\n\n"
        for transaction in history:
            if transaction.transaction_type == "deposit":
                history_text += (
                    f"{transaction.date.strftime('%Y-%m-%d %H:%M')} | "
                    f"Пополнение: +{transaction.amount:.2f} {transaction.currency_to}\n"
                )
            elif transaction.transaction_type == "withdraw":
                history_text += (
                    f"{transaction.date.strftime('%Y-%m-%d %H:%M')} | "
                    f"Снятие: -{transaction.amount:.2f} {transaction.currency_from}\n"
                )
            elif transaction.transaction_type == "transfer":
                if transaction.account_from == account_id:
                    if transaction.currency_from != transaction.currency_to:
                        history_text += (
                            f"{transaction.date.strftime('%Y-%m-%d %H:%M')} | "
                            f"Перевод на счет {transaction.account_to}: -{transaction.amount:.2f} {transaction.currency_from} "
                            f"(конвертировано по курсу {transaction.exchange_rate:.4f} -> "
                            f"{transaction.amount * transaction.exchange_rate:.2f} {transaction.currency_to})\n"
                        )
                    else:
                        history_text += (
                            f"{transaction.date.strftime('%Y-%m-%d %H:%M')} | "
                            f"Перевод на счет {transaction.account_to}: -{transaction.amount:.2f} {transaction.currency_from}\n"
                        )
                else:
                    if transaction.currency_from != transaction.currency_to:
                        history_text += (
                            f"{transaction.date.strftime('%Y-%m-%d %H:%M')} | "
                            f"Перевод со счета {transaction.account_from}: +{transaction.amount * transaction.exchange_rate:.2f} {transaction.currency_to} "
                            f"(конвертировано из {transaction.amount:.2f} {transaction.currency_from} "
                            f"по курсу {transaction.exchange_rate:.4f})\n"
                        )
                    else:
                        history_text += (
                            f"{transaction.date.strftime('%Y-%m-%d %H:%M')} | "
                            f"Перевод со счета {transaction.account_from}: +{transaction.amount:.2f} {transaction.currency_from}\n"
                        )

        messagebox.showinfo(f"История операций счета {account_id}", history_text)

    def _change_currency(self):
        if not self._check_auth():
            return

        account_id = self._get_account_id("Введите ID счета для изменения валюты:")
        if not account_id:
            return

        try:
            account_id = int(account_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID счета должен быть числом!")
            return

        current_currency = self.bank.get_account_currency(account_id)
        if not current_currency:
            messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])
            return

        currency_window = ctk.CTkToplevel(self.app)
        currency_window.title("Изменение валюты счета")
        currency_window.geometry("300x300")

        ctk.CTkLabel(
            currency_window,
            text=f"Текущая валюта: {current_currency}",
            font=self.title_font,
        ).pack(pady=10)

        ctk.CTkLabel(
            currency_window,
            text="Выберите новую валюту:",
            font=self.font_style,
        ).pack(pady=5)

        currencies = ["USD", "EUR", "GBP", "CNY", "RUB"]
        self.new_currency_var = ctk.StringVar(value=current_currency)

        for currency in currencies:
            if currency != current_currency:
                ctk.CTkRadioButton(
                    currency_window,
                    text=currency,
                    variable=self.new_currency_var,
                    value=currency,
                    font=self.font_style,
                ).pack(pady=2)

        ctk.CTkButton(
            currency_window,
            text="Изменить валюту",
            font=self.font_style,
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            command=lambda: self._apply_currency_change(
                account_id, current_currency, currency_window
            ),
        ).pack(pady=20)

    def _apply_currency_change(self, account_id, current_currency, window):
        new_currency = self.new_currency_var.get()

        if new_currency == current_currency:
            messagebox.showinfo("Информация", "Валюта не изменена")
            window.destroy()
            return

        try:
            exchange_rate = self.exchange_rates[current_currency][new_currency]
            if self.bank.convert_currency(account_id, new_currency, exchange_rate):
                messagebox.showinfo(
                    "Успех",
                    f"Валюта счета изменена на {new_currency}\n"
                    f"Курс обмена: 1 {current_currency} = {exchange_rate:.4f} {new_currency}",
                )
                window.destroy()
            else:
                messagebox.showerror("Ошибка", self.bank.error_handler.errors[-1])
        except KeyError:
            messagebox.showerror(
                "Ошибка", "Не удалось найти курс обмена для выбранных валют"
            )

    def _view_exchange_rates(self):
        rates_info = "Текущие курсы валют:\n\n"
        currencies = ["RUB", "USD", "EUR", "GBP", "CNY"]

        # Создаем заголовок таблицы
        rates_info += "{:8}".format("")
        for to_curr in currencies:
            rates_info += "{:8}".format(to_curr)
        rates_info += "\n"

        # Заполняем таблицу курсов
        for from_curr in currencies:
            rates_info += "{:8}".format(from_curr)
            for to_curr in currencies:
                if from_curr == to_curr:
                    rate = 1.0
                else:
                    rate = self.exchange_rates.get(from_curr, {}).get(to_curr, 0)
                rates_info += "{:8.4f}".format(rate)
            rates_info += "\n"

        messagebox.showinfo("Курсы валют", rates_info)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    BankingApp()
