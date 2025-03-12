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


app = ctk.CTk()
app.title("Банковская система")
app.geometry("400x700")

main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)


label_reg = ctk.CTkLabel(main_frame, text="Регистрация", font=("Arial", 16))
label_reg.grid(row=0, column=0, pady=10)

entry_name = ctk.CTkEntry(main_frame, placeholder_text="Имя")
entry_name.grid(row=1, column=0, pady=5)

entry_mail = ctk.CTkEntry(main_frame, placeholder_text="Почта")
entry_mail.grid(row=2, column=0, pady=5)

entry_password = ctk.CTkEntry(main_frame, placeholder_text="Пароль", show="*")
entry_password.grid(row=3, column=0, pady=5)

button_reg = ctk.CTkButton(main_frame, text="Зарегистрироваться", command=register_user)
button_reg.grid(row=4, column=0, pady=10)

label_auth = ctk.CTkLabel(main_frame, text="Аутентификация", font=("Arial", 16))
label_auth.grid(row=5, column=0, pady=10)

entry_auth_mail = ctk.CTkEntry(main_frame, placeholder_text="Почта")
entry_auth_mail.grid(row=6, column=0, pady=5)

entry_auth_password = ctk.CTkEntry(main_frame, placeholder_text="Пароль", show="*")
entry_auth_password.grid(row=7, column=0, pady=5)

button_auth = ctk.CTkButton(main_frame, text="Войти", command=authenticate_user)
button_auth.grid(row=8, column=0, pady=10)

label_operations = ctk.CTkLabel(main_frame, text="Операции со счетом", font=("Arial", 16))
label_operations.grid(row=9, column=0, pady=10)

button_create_account = ctk.CTkButton(main_frame, text="Создать счет", command=create_account)
button_create_account.grid(row=10, column=0, pady=5)

button_deposit = ctk.CTkButton(main_frame, text="Пополнить счет", command=deposit)
button_deposit.grid(row=11, column=0, pady=5)

button_withdraw = ctk.CTkButton(main_frame, text="Снять средства", command=withdraw)
button_withdraw.grid(row=12, column=0, pady=5)

button_transfer = ctk.CTkButton(main_frame, text="Перевести средства", command=transfer)
button_transfer.grid(row=13, column=0, pady=5)

button_balance = ctk.CTkButton(main_frame, text="Просмотреть баланс", command=get_balance)
button_balance.grid(row=14, column=0, pady=5)

app.mainloop()