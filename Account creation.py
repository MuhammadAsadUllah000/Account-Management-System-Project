import tkinter as tk
import sqlite3
from tkinter import simpledialog, messagebox

class Account:
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

    def display_balance(self):
        return f"Account: {self.name}, Balance: {self.balance}"


class AccountManager:
    def __init__(self):
        self.conn = sqlite3.connect('accounts.db')
        self.create_table()
        self.load_accounts()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def load_accounts(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, balance FROM accounts')
        rows = cursor.fetchall()
        self.accounts = [Account(id, name, balance) for id, name, balance in rows]

    def create_account(self, name, balance):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO accounts (name, balance) VALUES (?, ?)', (name, balance))
        self.conn.commit()
        self.load_accounts()
        return f"Account {name} created successfully."

    def delete_account(self, id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM accounts WHERE id = ?', (id,))
        self.conn.commit()
        self.load_accounts()
        return f"Account deleted successfully."

    def get_account(self, name):
        for account in self.accounts:
            if account.name == name:
                return account
        return None


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Account Manager")

        self.manager = AccountManager()

        self.label = tk.Label(self, text="Welcome to Account Manager", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.create_account_button = tk.Button(self, text="Create Account", command=self.create_account)
        self.create_account_button.pack(pady=5)

        self.delete_account_button = tk.Button(self, text="Delete Account", command=self.delete_account)
        self.delete_account_button.pack(pady=5)

        self.deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(pady=5)

        self.balance_button = tk.Button(self, text="Display Balance", command=self.display_balance)
        self.balance_button.pack(pady=5)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

    def create_account(self):
        name = self.prompt("Enter account name:")
        balance = float(self.prompt("Enter initial balance:"))
        result = self.manager.create_account(name, balance)
        self.display_message(result)

    def delete_account(self):
        name = self.prompt("Enter account name to delete:")
        account = self.manager.get_account(name)
        if account:
            result = self.manager.delete_account(account.id)
            self.display_message(result)
        else:
            self.display_message(f"Account {name} not found.")

    def deposit(self):
        name = self.prompt("Enter account name:")
        account = self.manager.get_account(name)
        if account:
            amount = float(self.prompt("Enter amount to deposit:"))
            account.deposit(amount)
            self.display_message(account.display_balance())
        else:
            self.display_message(f"Account {name} not found.")

    def withdraw(self):
        name = self.prompt("Enter account name:")
        account = self.manager.get_account(name)
        if account:
            amount = float(self.prompt("Enter amount to withdraw:"))
            success = account.withdraw(amount)
            if success:
                self.display_message(account.display_balance())
            else:
                self.display_message("Insufficient funds.")
        else:
            self.display_message(f"Account {name} not found.")

    def display_balance(self):
        name = self.prompt("Enter account name:")
        account = self.manager.get_account(name)
        if account:
            self.display_message(account.display_balance())
        else:
            self.display_message(f"Account {name} not found.")

    def prompt(self, message):
        return simpledialog.askstring("Input", message)

    def display_message(self, message):
        messagebox.showinfo("Result", message)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
