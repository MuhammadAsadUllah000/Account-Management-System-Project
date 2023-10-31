import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import ttk, simpledialog
from tkinter import Entry, Tk
import datetime 
from tkinter import simpledialog, messagebox
import sqlite3

class Account:
    def __init__(self, id, name, balance, password):
        self.id = id
        self.name = name
        self.balance = balance
        self.password = password

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
                balance REAL NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def load_accounts(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, balance, password FROM accounts')
        rows = cursor.fetchall()
        self.accounts = [Account(id, name, balance, password) for id, name, balance, password in rows]

    def create_account(self, name, balance, password):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO accounts (name, balance, password) VALUES (?, ?, ?)', (name, balance, password))
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

    def check_password(self, name, password):
        account = self.get_account(name)
        if account and account.password == password:
            return True
        return False

class FinancialManagementWindow(tk.Toplevel):
    def __init__(self, manager):
        super().__init__()

        self.title("Financial Management System")
        self.manager = manager

        self.label = tk.Label(self, text="Welcome to Financial Management", font=("Helvetica", 16))
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
        password = self.prompt("Set account password:")
        result = self.manager.create_account(name, balance, password)
        self.display_message(result)

    def delete_account(self):
        name = self.prompt("Enter account name to delete:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
            account = self.manager.get_account(name)
            if account:
                result = self.manager.delete_account(account.id)
                self.display_message(result)
            else:
                self.display_message(f"Account {name} not found.")
        else:
            self.display_message("Invalid password")

    def deposit(self):
        name = self.prompt("Enter account name:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
            account = self.manager.get_account(name)
            if account:
                amount = float(self.prompt("Enter amount to deposit:"))
                account.deposit(amount)
                self.display_message(account.display_balance())
            else:
                self.display_message(f"Account {name} not found.")
        else:
            self.display_message("Invalid password")

    def withdraw(self):
        name = self.prompt("Enter account name:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
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
        else:
            self.display_message("Invalid password")

    def display_balance(self):
        name = self.prompt("Enter account name:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
            account = self.manager.get_account(name)
            if account:
                self.display_message(account.display_balance())
            else:
                self.display_message(f"Account {name} not found.")
        else:
            self.display_message("Invalid password")

    def prompt(self, message):
        return simpledialog.askstring("Input", message, show='*')

    def display_message(self, message):
        messagebox.showinfo("Result", message)

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

        self.financial_management_button = tk.Button(self, text="Financial Management", command=self.open_financial_management)
        self.financial_management_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

    def create_account(self):
        name = self.prompt("Enter account name:")
        balance = float(self.prompt("Enter initial balance:"))
        password = self.prompt("Set account password:")
        result = self.manager.create_account(name, balance, password)
        self.display_message(result)

    def delete_account(self):
        name = self.prompt("Enter account name to delete:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
            account = self.manager.get_account(name)
            if account:
                result = self.manager.delete_account(account.id)
                self.display_message(result)
            else:
                self.display_message(f"Account {name} not found.")
        else:
            self.display_message("Invalid password")

    def deposit(self):
        name = self.prompt("Enter account name:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
            account = self.manager.get_account(name)
            if account:
                amount = float(self.prompt("Enter amount to deposit:"))
                account.deposit(amount)
                self.display_message(account.display_balance())
            else:
                self.display_message(f"Account {name} not found.")
        else:
            self.display_message("Invalid password")

    def withdraw(self):
        name = self.prompt("Enter account name:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
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
        else:
            self.display_message("Invalid password")

    def display_balance(self):
        name = self.prompt("Enter account name:")
        password = self.prompt("Enter account password:")
        if self.manager.check_password(name, password):
            account = self.manager.get_account(name)
            if account:
                self.display_message(account.display_balance())
            else:
                self.display_message(f"Account {name} not found.")
        else:
            self.display_message("Invalid password")

    def open_financial_management(self):
        financial_management_window = FinancialManagementWindow(self.manager)

    def prompt(self, message):
        return simpledialog.askstring("Input", message, show='*')

    def display_message(self, message):
        messagebox.showinfo("Result", message)



id_counter = 0
employees = {}
timetable_id_counter = 0
timetables = {}
attendance_records = {}

def generate_unique_id():
    global id_counter
    id_counter += 1
    return id_counter

# ... (rest of your code)


def open_employee_management():


    def generate_unique_id():
        global id_counter
        id_counter += 1
        return id_counter

    def add_employee():
        # ... (rest of your add_employee code)
        global name_entry, experience_entry, designation_entry, salary_entry, address_entry, contact_entry, email_entry, result_display
        
        name = name_entry.get()
        experience = experience_entry.get()
        designation = designation_entry.get()
        salary = salary_entry.get()
        home_address = address_entry.get()
        contact_number = contact_entry.get()
        email = email_entry.get()

        if not all([name, experience, designation, salary, home_address, contact_number, email]):
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "All fields are required!")
            return

        id = generate_unique_id()  # Generate a unique ID
        employees[id] = {
            'Name': name,
            'Experience': experience,
            'Designation': designation,
            'Salary': salary,
            'Personal Information': {
                'Home Address': home_address,
                'Contact Number': contact_number,
                'Email': email
            }
        }

        # Clear entry fields after adding employee
        name_entry.delete(0, tk.END)
        experience_entry.delete(0, tk.END)
        designation_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    def search_employee_by_name():
        # ... (rest of your search_employee_by_name code)
        global result_display
        name_to_search = simpledialog.askstring("Search Employee", "Enter employee name:")
        if name_to_search:
            found = False
            for emp_id, emp_info in employees.items():
                if emp_info['Name'] == name_to_search:
                    display_employee_info(emp_id, emp_info)
                    found = True
                    break
            if not found:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with the name '{name_to_search}'\n")

    def search_employee_by_id():
        
        global result_display

        id_to_search = simpledialog.askinteger("Search Employee", "Enter employee ID:")
        if id_to_search:
            emp_info = employees.get(id_to_search)
            if emp_info:
                display_employee_info(id_to_search, emp_info)
            else:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with the ID '{id_to_search}'\n")

    def display_employee_info(emp_id, emp_info):
        # ... (rest of your display_employee_info code)
        global result_display

        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, f"ID: {emp_id}\n")
        for key, value in emp_info.items():
            if key == 'Personal Information':
                result_display.insert(tk.END, f"{key}:\n")
                for info_key, info_value in value.items():
                    result_display.insert(tk.END, f"\t{info_key}: {info_value}\n")
            else:
                result_display.insert(tk.END, f"{key}: {value}\n")

    def edit_employee():
        # ... (rest of your edit_employee code)
        global result_display

        id_to_edit = simpledialog.askinteger("Edit Employee Data", "Enter employee ID:")
        if id_to_edit:
            emp_info = employees.get(id_to_edit)
            if emp_info:
                edit_employee_window = tk.Toplevel(root)
                edit_employee_window.title(f"Edit Employee Data {id_to_edit}")

                name_var = tk.StringVar(value=emp_info['Name'])
                experience_var = tk.StringVar(value=emp_info['Experience'])
                designation_var = tk.StringVar(value=emp_info['Designation'])
                salary_var = tk.StringVar(value=emp_info['Salary'])
                address_var = tk.StringVar(value=emp_info['Personal Information']['Home Address'])
                contact_var = tk.StringVar(value=emp_info['Personal Information']['Contact Number'])
                email_var = tk.StringVar(value=emp_info['Personal Information']['Email'])

                ttk.Label(edit_employee_window, text="Name:", font=font_style).grid(row=0, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

                ttk.Label(edit_employee_window, text="Experience:", font=font_style).grid(row=1, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=experience_var).grid(row=1, column=1, padx=5, pady=5)

                ttk.Label(edit_employee_window, text="Designation:", font=font_style).grid(row=2, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=designation_var).grid(row=2, column=1, padx=5, pady=5)

                ttk.Label(edit_employee_window, text="Salary:", font=font_style).grid(row=3, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=salary_var).grid(row=3, column=1, padx=5, pady=5)

                ttk.Label(edit_employee_window, text="Home Address:", font=font_style).grid(row=4, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=address_var).grid(row=4, column=1, padx=5, pady=5)

                ttk.Label(edit_employee_window, text="Contact Number:", font=font_style).grid(row=5, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=contact_var).grid(row=5, column=1, padx=5, pady=5)

                ttk.Label(edit_employee_window, text="Email Address:", font=font_style).grid(row=6, column=0, padx=5, pady=5, sticky='e')
                ttk.Entry(edit_employee_window, font=font_style, textvariable=email_var).grid(row=6, column=1, padx=5, pady=5)

            def save_changes():
                employees[id_to_edit]['Name'] = name_var.get()
                employees[id_to_edit]['Experience'] = experience_var.get()
                employees[id_to_edit]['Designation'] = designation_var.get()
                employees[id_to_edit]['Salary'] = salary_var.get()
                employees[id_to_edit]['Personal Information']['Home Address'] = address_var.get()
                employees[id_to_edit]['Personal Information']['Contact Number'] = contact_var.get()
                employees[id_to_edit]['Personal Information']['Email'] = email_var.get()
                edit_employee_window.destroy()

            save_button = ttk.Button(edit_employee_window, text="Save Changes", command=save_changes)
            save_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"No employee found with the ID '{id_to_edit}'\n")

    def generate_unique_timetable_id():
        global timetable_id_counter
        timetable_id_counter += 1
        return timetable_id_counter

    def add_timetable():
        # ... (rest of your add_timetable code)
        global id_entry, result_display, monday_var, tuesday_var, wednesday_var, thursday_var, friday_var

        emp_id = id_entry.get()
        working_hours = [monday_var.get(), tuesday_var.get(), wednesday_var.get(), thursday_var.get(), friday_var.get()]

        if not all([emp_id, *working_hours]):
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Employee ID and all working hours are required!")
            return

        emp_id = int(emp_id)
        if emp_id not in employees:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"No employee found with ID '{emp_id}'")
            return

        if emp_id in timetables:
            timetables[emp_id].extend(working_hours)
        else:
            timetables[emp_id] = working_hours

        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, "Working hours added successfully!")

        # Clear entry fields
        id_entry.delete(0, tk.END)
        monday_var.delete(0, tk.END)
        tuesday_var.delete(0, tk.END)
        wednesday_var.delete(0, tk.END)
        thursday_var.delete(0, tk.END)
        friday_var.delete(0, tk.END)

        display_employee_timetable(emp_id)

    def display_employee_timetable():
        # ... (rest of your display_employee_timetable code)
        global result_display

        emp_id = simpledialog.askinteger("Display Timetable", "Enter employee ID:")
        if emp_id:
            if emp_id in employees:
                emp_info = employees[emp_id]
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"\nEmployee Name: {emp_info['Name']}\n")
                if emp_id in timetables:
                    result_display.insert(tk.END, f"Timetable for Employee ID {emp_id}:\n")
                    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                    timetable = timetables[emp_id]
                    for day, hours in zip(days, timetable):
                        result_display.insert(tk.END, f"{day}: {hours}\n")
                else:
                    result_display.insert(tk.END, f"No timetable found for Employee ID {emp_id}\n")
            else:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with the ID '{emp_id}'\n")

    def open_attendance_window():
        record_attendance()

    def record_attendance():
        # ... (rest of your record_attendance code)
        global id_entry, result_display, attendance_var, attendance_window

        attendance_window = tk.Toplevel(root)
        attendance_window.title("Record Attendance")

        ttk.Label(attendance_window, text="Enter Employee ID*:", font=font_style).grid(row=0, column=0, padx=(5, 2), pady=5, sticky='e')
        id_entry = ttk.Entry(attendance_window, font=font_style)
        id_entry.grid(row=0, column=1, padx=(2, 5), pady=5)
        ttk.Label(attendance_window, text="*", font=font_style, foreground="red").grid(row=0, column=2, padx=5, pady=5, sticky='w')

        attendance_var = tk.StringVar(value="")  # Initialize as empty

        ttk.Radiobutton(attendance_window, text="Present", variable=attendance_var, value="Present").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(attendance_window, text="Absent", variable=attendance_var, value="Absent").grid(row=2, column=0, padx=5, pady=5, sticky='w')

    def display_attendance():
        emp_id = id_entry.get()
        if emp_id:
            emp_id = int(emp_id)
            if emp_id in employees:
                result_display.delete(1.0, tk.END)
                if emp_id in attendance_records:
                    result_display.insert(tk.END, f"Attendance Record for Employee ID {emp_id}:\n")
                    for date, status in attendance_records[emp_id].items():
                        result_display.insert(tk.END, f"Date: {date}, Status: {status}\n")
                else:
                    result_display.insert(tk.END, f"No attendance record found for Employee ID {emp_id}\n")
            else:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with ID '{emp_id}'\n")
        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Please enter Employee ID\n")

        display_button = ttk.Button(attendance_window, text="Display Attendance", command=display_attendance)
        display_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        result_display = tk.Text(attendance_window, height=5, width=40)
        result_display.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def save_attendance():
        emp_id = id_entry.get()
        attendance = attendance_var.get()

        if emp_id and attendance:
            emp_id = int(emp_id)
            if emp_id in employees:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"Attendance for Employee ID {emp_id}: {attendance}\n")
                # Add attendance record
                if emp_id not in attendance_records:
                    attendance_records[emp_id] = {}
                today = datetime.date.today().isoformat()
                attendance_records[emp_id][today] = attendance
            else:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with ID '{emp_id}'\n")
        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Please enter Employee ID and select either 'Present' or 'Absent'\n")

        save_button = ttk.Button(attendance_window, text="Save Attendance", command=save_attendance)
        save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)



    

    result_display = None

    def open_health_benefits_window():
        # ... (rest of your open_health_benefits_window code)
        global health_care_var, paid_time_off_var, retirement_contrib_var, childcare_contrib_var, tuition_reimb_var, id_entry, result_display

        health_benefits_window = tk.Toplevel(root)
        health_benefits_window.title("Manage Health Benefits")

        ttk.Label(health_benefits_window, text="Enter Employee ID*:", font=font_style).pack(anchor='w', pady=(10, 0))
        id_entry = ttk.Entry(health_benefits_window, font=font_style)
        id_entry.pack(anchor='w', padx=10)
        ttk.Label(health_benefits_window, text="*", font=font_style, foreground="red").pack(anchor='w', padx=(0, 10))

        health_care_var = tk.BooleanVar(value=False)
        paid_time_off_var = tk.BooleanVar(value=False)
        retirement_contrib_var = tk.BooleanVar(value=False)
        childcare_contrib_var = tk.BooleanVar(value=False)
        tuition_reimb_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(health_benefits_window, text="Health Care Coverage", variable=health_care_var).pack(anchor='w')
        ttk.Checkbutton(health_benefits_window, text="Paid Time Off", variable=paid_time_off_var).pack(anchor='w')
        ttk.Checkbutton(health_benefits_window, text="Retirement Contributions and Plans", variable=retirement_contrib_var).pack(anchor='w')
        ttk.Checkbutton(health_benefits_window, text="Childcare Contributions", variable=childcare_contrib_var).pack(anchor='w')
        ttk.Checkbutton(health_benefits_window, text="Tuition Reimbursement", variable=tuition_reimb_var).pack(anchor='w')

        save_button = ttk.Button(health_benefits_window, text="Save", command=save_health_benefits)
        save_button.pack(pady=10)

        display_button = ttk.Button(health_benefits_window, text="Display", command=display_health_benefits)
        display_button.pack(pady=10)

        # Add a text widget for displaying results
        result_display = tk.Text(health_benefits_window, wrap="word", width=50, height=10, state=tk.DISABLED)
        result_display.pack(padx=10, pady=(0, 10))


    def save_health_benefits():
        # ... (rest of your save_health_benefits code)
        global result_display
        emp_id = id_entry.get()
        health_care = health_care_var.get()
        paid_time_off = paid_time_off_var.get()
        retirement_contrib = retirement_contrib_var.get()
        childcare_contrib = childcare_contrib_var.get()
        tuition_reimb = tuition_reimb_var.get()

        if emp_id and (health_care or paid_time_off or retirement_contrib or childcare_contrib or tuition_reimb):
            emp_id = int(emp_id)
            if emp_id in employees:
                # Now you can save the health benefits for the specific employee.
                # For example, you can create a dictionary to store the benefits.
                employee_health_benefits = {
                    'Health Care Coverage': health_care,
                    'Paid Time Off': paid_time_off,
                    'Retirement Contributions': retirement_contrib,
                    'Childcare Contributions': childcare_contrib,
                    'Tuition Reimbursement': tuition_reimb
                }

                # Add the health benefits to the employee's information.
                if 'Health Benefits' not in employees[emp_id]:
                    employees[emp_id]['Health Benefits'] = {}
                employees[emp_id]['Health Benefits'] = employee_health_benefits

                # Clear entry fields and checkboxes
                id_entry.delete(0, tk.END)
                health_care_var.set(False)
                paid_time_off_var.set(False)
                retirement_contrib_var.set(False)
                childcare_contrib_var.set(False)
                tuition_reimb_var.set(False)

                result_display.config(state=tk.NORMAL)
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"Health benefits saved for Employee ID {emp_id}\n")
                result_display.config(state=tk.DISABLED)
            else:
                result_display.config(state=tk.NORMAL)
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with ID '{emp_id}'\n")
                result_display.config(state=tk.DISABLED)
        else:
            result_display.config(state=tk.NORMAL)
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Please enter Employee ID and select at least one health benefit option\n")
            result_display.config(state=tk.DISABLED)

    def display_health_benefits():
        # ... (rest of your display_health_benefits code)
        global result_display
        emp_id = id_entry.get()
        if emp_id:
            emp_id = int(emp_id)
            if emp_id in employees and 'Health Benefits' in employees[emp_id]:
                benefits = employees[emp_id]['Health Benefits']
                result_display.config(state=tk.NORMAL)
                result_display.delete(1.0, tk.END)

                # Get the employee's name
                emp_name = employees[emp_id]['Name']

                result_display.insert(tk.END, f"\nHealth Benefits for Employee ID {emp_id} ({emp_name}):\n")
                for benefit, value in benefits.items():
                    result_display.insert(tk.END, f"{benefit}: {'Yes' if value else 'No'}\n")
                result_display.config(state=tk.DISABLED)
            else:
                result_display.config(state=tk.NORMAL)
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No health benefits found for Employee ID {emp_id}\n")
                result_display.config(state=tk.DISABLED)
        else:
            result_display.config(state=tk.NORMAL)
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Please enter Employee ID\n")
            result_display.config(state=tk.DISABLED)

    def open_add_staffing_window():
        # ... (rest of your open_add_staffing_window code)
        global name_entry, experience_entry, designation_entry, salary_entry, address_entry, contact_entry, email_entry, result_display

        add_staffing_window = tk.Toplevel(root)
        add_staffing_window.title("Add Staffing")

        # Labels and Entry fields with red asterisks
        ttk.Label(add_staffing_window, text="Name*:", font=font_style).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        name_entry = ttk.Entry(add_staffing_window, font=font_style)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=0, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(add_staffing_window, text="Experience*:", font=font_style).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        experience_entry = ttk.Entry(add_staffing_window, font=font_style)
        experience_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=1, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(add_staffing_window, text="Designation*:", font=font_style).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        designation_entry = ttk.Entry(add_staffing_window, font=font_style)
        designation_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=2, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(add_staffing_window, text="Salary*:", font=font_style).grid(row=3, column=0, padx=5, pady=5, sticky='e')
        salary_entry = ttk.Entry(add_staffing_window, font=font_style)
        salary_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=3, column=2, padx=5, pady=5, sticky='w')

        personal_info_label = ttk.Label(add_staffing_window, text="Personal Information")
        personal_info_label.grid(row=4, column=0, columnspan=3, pady=5, sticky='w', padx=5)

        ttk.Label(add_staffing_window, text="Home Address*:", font=font_style).grid(row=5, column=0, padx=5, pady=5, sticky='e')
        address_entry = ttk.Entry(add_staffing_window, font=font_style)
        address_entry.grid(row=5, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=5, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(add_staffing_window, text="Contact Number*:", font=font_style).grid(row=6, column=0, padx=5, pady=5, sticky='e')
        contact_entry = ttk.Entry(add_staffing_window, font=font_style)
        contact_entry.grid(row=6, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=6, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(add_staffing_window, text="Email Address*:", font=font_style).grid(row=7, column=0, padx=5, pady=5, sticky='e')
        email_entry = ttk.Entry(add_staffing_window, font=font_style)
        email_entry.grid(row=7, column=1, padx=5, pady=5)
        ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=7, column=2, padx=5, pady=5, sticky='w')

        add_button = ttk.Button(add_staffing_window, text="Add Employee", command=add_employee)
        add_button.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

        search_by_name_button = ttk.Button(add_staffing_window, text="Search by Name", command=search_employee_by_name)
        search_by_name_button.grid(row=9, column=0, padx=5, pady=5)

        search_by_id_button = ttk.Button(add_staffing_window, text="Search by ID", command=search_employee_by_id)
        search_by_id_button.grid(row=9, column=1, padx=5, pady=5)

        result_display = tk.Text(add_staffing_window, height=10, width=40)
        result_display.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

    def open_timetable_window():
        # ... (rest of your open_timetable_window code)
        global id_entry, result_display, monday_var, tuesday_var, wednesday_var, thursday_var, friday_var

        timetable_window = tk.Toplevel(root)
        timetable_window.title("Employee Timetable")

        ttk.Label(timetable_window, text="Enter Employee ID*:", font=font_style).grid(row=0, column=0, padx=(5, 2), pady=5, sticky='e')
        id_entry = ttk.Entry(timetable_window, font=font_style)
        id_entry.grid(row=0, column=1, padx=(2, 5), pady=5)
        ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=0, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(timetable_window, text="Working Hours:", font=font_style).grid(row=1, column=0, padx=(5, 2), pady=5, sticky='e')

        ttk.Label(timetable_window, text="Monday*:", font=font_style).grid(row=1, column=1, padx=(2, 5), pady=5, sticky='w')
        monday_var = ttk.Entry(timetable_window, font=font_style, width=8)
        monday_var.grid(row=1, column=2, padx=(2, 5), pady=5)
        ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(timetable_window, text="Tuesday*:", font=font_style).grid(row=1, column=4, padx=(2, 5), pady=5, sticky='w')
        tuesday_var = ttk.Entry(timetable_window, font=font_style, width=8)
        tuesday_var.grid(row=1, column=5, padx=(2, 5), pady=5)
        ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=6, padx=5, pady=5, sticky='w')

        ttk.Label(timetable_window, text="Wednesday*:", font=font_style).grid(row=1, column=7, padx=(2, 5), pady=5, sticky='w')
        wednesday_var = ttk.Entry(timetable_window, font=font_style, width=8)
        wednesday_var.grid(row=1, column=8, padx=(2, 5), pady=5)
        ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=9, padx=5, pady=5, sticky='w')

        ttk.Label(timetable_window, text="Thursday*:", font=font_style).grid(row=1, column=10, padx=(2, 5), pady=5, sticky='w')
        thursday_var = ttk.Entry(timetable_window, font=font_style, width=8)
        thursday_var.grid(row=1, column=11, padx=(2, 5), pady=5)
        ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=12, padx=5, pady=5, sticky='w')

        ttk.Label(timetable_window, text="Friday*:", font=font_style).grid(row=1, column=13, padx=(2, 5), pady=5, sticky='w')
        friday_var = ttk.Entry(timetable_window, font=font_style, width=8)
        friday_var.grid(row=1, column=14, padx=(2, 5), pady=5)
        ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=15, padx=5, pady=5, sticky='w')

        add_button = ttk.Button(timetable_window, text="Add Timetable", command=add_timetable)
        add_button.grid(row=2, column=0, columnspan=16, padx=5, pady=5)

        display_button = ttk.Button(timetable_window, text="Display Timetable", command=display_employee_timetable)
        display_button.grid(row=3, column=0, columnspan=16, padx=5, pady=5)

        result_display = tk.Text(timetable_window, height=10, width=60)
        result_display.grid(row=4, column=0, columnspan=16, padx=5, pady=5)

    root = tk.Tk()
    root.title("Employee Management System")

    font_style = ('Arial', 12)

    menu_bar = tk.Menu(root)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)

    employee_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Employee", menu=employee_menu)
    employee_menu.add_command(label="Add Staffing", command=open_add_staffing_window)
    employee_menu.add_command(label="Edit Staffing", command=edit_employee)

    timetable_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Timetable", menu=timetable_menu)
    timetable_menu.add_command(label="Employee Timetable", command=open_timetable_window)

    attendance_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Attendance", menu=attendance_menu)
    attendance_menu.add_command(label="Record Attendance", command=open_attendance_window)

    health_benefits_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Health Benefits", menu=health_benefits_menu)
    health_benefits_menu.add_command(label="Manage Health Benefits", command=open_health_benefits_window)

    root.config(menu=menu_bar)

class Product:
    def __init__(self, name, price, quantity, supplier, image_path):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier
        self.purchased_quantity = quantity  # Set purchased_quantity to the initial quantity
        self.sold_quantity = 0
        self.image_path = image_path

    def purchase(self, quantity):
        self.quantity += quantity
        self.purchased_quantity += quantity

    def sell(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.sold_quantity += quantity
        else:
            messagebox.showerror("Error", "Insufficient quantity in stock.")

    @property
    def remaining_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Name: {self.name}, Price: ${self.price}, Quantity: {self.quantity}, Supplier: {self.supplier}"

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def view_stock(self):
        return self.products

    def record_stock(self, product_name, quantity):
        for product in self.products:
            if product.name == product_name:
                product.purchase(quantity)
                print(f"Purchased {quantity} units of {product_name}")
                return
        print(f"Product '{product_name}' not found")

def add_stock(name_entry, price_entry, quantity_entry, supplier_entry, add_stock_window, image_path):
    name = name_entry.get()
    price = float(price_entry.get())
    quantity = int(quantity_entry.get())
    supplier = supplier_entry.get()

    product = Product(name, price, quantity, supplier, image_path)
    inventory.add_product(product)

    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    supplier_entry.delete(0, tk.END)

    add_stock_window.destroy()


def open_add_stock_window():
    add_stock_window = tk.Toplevel(root)
    add_stock_window.title("Add Stock")

    def add_image():
        global image_path
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        image_label.config(text=f"Image Path: {image_path}")

    name_label = tk.Label(add_stock_window, text="Product Name*")
    price_label = tk.Label(add_stock_window, text="Price*")
    quantity_label = tk.Label(add_stock_window, text="Purchased Quantity*")
    supplier_label = tk.Label(add_stock_window, text="Supplier*")

    name_entry = tk.Entry(add_stock_window)
    price_entry = tk.Entry(add_stock_window)
    quantity_entry = tk.Entry(add_stock_window)
    supplier_entry = tk.Entry(add_stock_window)

    add_image_button = tk.Button(add_stock_window, text="Add Image", command=add_image)
    add_button = tk.Button(add_stock_window, text="Add Stock", command=lambda: add_stock(name_entry, price_entry, quantity_entry, supplier_entry, add_stock_window, image_path))

    required_label = tk.Label(add_stock_window, text="* Required Field", fg="red")
    required_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=5)

    required_label.grid(row=0, column=2, sticky="w")
    name_label.grid(row=0, column=0)
    price_label.grid(row=1, column=0)
    quantity_label.grid(row=2, column=0)
    supplier_label.grid(row=3, column=0)

    name_entry.grid(row=0, column=1)
    price_entry.grid(row=1, column=1)
    quantity_entry.grid(row=2, column=1)
    supplier_entry.grid(row=3, column=1)

    add_image_button.grid(row=4, column=0, columnspan=2, pady=10)
    add_button.grid(row=5, column=0, columnspan=2, pady=10)

    image_label = tk.Label(add_stock_window, text="Image Path:")
    image_label.grid(row=6, column=0, columnspan=2, pady=5)

def open_view_stock_window():
    view_stock_window = tk.Toplevel(root)
    view_stock_window.title("View Stock")

    label = tk.Label(view_stock_window, text="Enter Product Name:")
    entry = tk.Entry(view_stock_window)
    entry.pack(pady=10)
    label.pack(pady=5)

    def view_product():
     name = entry.get()
     product = None
     for p in inventory.products:
        if p.name == name:
            product = p
            break
     if product:
        result_frame = tk.Frame(view_stock_window)
        result_frame.pack(pady=10)

        tk.Label(result_frame, text="Name:").grid(row=0, column=0, sticky='w')
        tk.Label(result_frame, text=product.name).grid(row=0, column=1, sticky='w')

        tk.Label(result_frame, text="Price:").grid(row=1, column=0, sticky='w')
        tk.Label(result_frame, text=f"${product.price}").grid(row=1, column=1, sticky='w')

        tk.Label(result_frame, text="Quantity:").grid(row=2, column=0, sticky='w')
        tk.Label(result_frame, text=product.quantity).grid(row=2, column=1, sticky='w')

        tk.Label(result_frame, text="Supplier:").grid(row=3, column=0, sticky='w')
        tk.Label(result_frame, text=product.supplier).grid(row=3, column=1, sticky='w')

        # Display the image in a small box
        img = Image.open(product.image_path)
        img = img.resize((100, 100))  # Resize the image
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(result_frame, image=photo)
        img_label.image = photo  # Keep a reference to prevent garbage collection
        img_label.grid(row=4, column=0, columnspan=2, pady=5)

     else:
        messagebox.showerror("Error", f"No stock or product found with the name '{name}'")



    view_button = tk.Button(view_stock_window, text="View Product", command=view_product)
    view_button.pack(pady=10)

def open_record_stock_window():
    record_stock_window = tk.Toplevel(root)
    record_stock_window.title("Record Stock")

    name_label = tk.Label(record_stock_window, text="Product Name")
    name_entry = tk.Entry(record_stock_window)

    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)

    display_button = tk.Button(record_stock_window, text="Display Records", command=lambda: display_records(record_stock_window, name_entry.get()))
    display_button.grid(row=1, columnspan=2, pady=10)

def record_stock(name_entry, quantity_entry):
    name = name_entry.get()
    quantity = int(quantity_entry.get())
    inventory.record_stock(name, quantity)
    print(f"Recorded {quantity} units of {name}")

def display_records(record_stock_window, product_name):
    for product in inventory.products:
        if product.name == product_name:
            labels = ['Purchased', 'Sold', 'Remaining']
            quantities = [product.purchased_quantity, product.sold_quantity, product.remaining_quantity]

            plt.figure(figsize=(8, 6))
            plt.bar(labels, quantities, color=['blue', 'green', 'red'])
            plt.xlabel('Operation')
            plt.ylabel('Quantity')
            plt.title(f'Records for {product.name}')
            plt.show()
            return

    messagebox.showerror("Error", f"Product '{product_name}' not found.")

def reorder_product(product_name, quantity, name_entry, quantity_entry, result_label):
    for product in inventory.products:
        if product.name == product_name:
            product.quantity += quantity
            print(f"Reordered {product.name}, New Quantity: {product.quantity}")
            result_label.config(text=f"Reordered {product.name}, New Quantity: {product.quantity}")
            name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            return
    else:
                result_label.config(text=f"Product '{product_name}' not found")  # Display error message in the label

def open_reorder_window():
    reorder_window = tk.Toplevel(root)
    reorder_window.title("Reorder")

    inventory_list = inventory.view_stock()

    def reorder_and_close():
        product_name = name_entry.get()
        quantity = int(quantity_entry.get())

        if not product_name or not quantity:
            messagebox.showerror("Error", "Both fields are required.")
            return

        reorder_product(product_name, quantity, name_entry, quantity_entry, result_label)

    name_label = tk.Label(reorder_window, text="Product Name")
    name_entry = tk.Entry(reorder_window)
    name_label.pack(pady=5)
    name_entry.pack(pady=5)

    quantity_label = tk.Label(reorder_window, text="Reorder Quantity")
    quantity_entry = tk.Entry(reorder_window)
    quantity_label.pack(pady=5)
    quantity_entry.pack(pady=5)

    reorder_button = tk.Button(reorder_window, text="Reorder", command=reorder_and_close)
    reorder_button.pack(pady=10)

    result_label = tk.Label(reorder_window, text="", font=('Arial', 12))
    result_label.pack(pady=10)

def open_product_info_window():
    product_info_window = tk.Toplevel(root)
    product_info_window.title("Product Information")

    name_label = tk.Label(product_info_window, text="Product Name")
    name_entry = tk.Entry(product_info_window)
    name_entry.pack(pady=10)

    info_label = tk.Label(product_info_window, text="", font=('Arial', 12))
    info_label.pack(pady=10)

    info_button = tk.Button(product_info_window, text="Get Product Information", command=lambda: product_info(name_entry.get(), info_label))
    info_button.pack(pady=10)

def product_info(name, info_label):
    info = ""
    for product in inventory.products:
        if product.name == name:
            info = f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Supplier: {product.supplier}"
            break

    if info:
        info_label.config(text=info)  # Update label in the GUI
    else:
        error_message = f"Product '{name}' not found"
        info_label.config(text=error_message)  # Display error message in the label

def update_listbox():
    open_view_stock_window()
def open_inventory_management():
    inventory_management_window = tk.Toplevel(root)
    inventory_management_window.title("Inventory Management")

    add_stock_button = tk.Button(inventory_management_window, text="Add Stock", command=open_add_stock_window)
    view_stock_button = tk.Button(inventory_management_window, text="View Stock", command=open_view_stock_window)
    record_stock_button = tk.Button(inventory_management_window, text="Record Stock", command=open_record_stock_window)
    reorder_button = tk.Button(inventory_management_window, text="Reordering", command=open_reorder_window)
    product_info_button = tk.Button(inventory_management_window, text="Product Information", command=open_product_info_window)

    add_stock_button.pack(side=tk.LEFT, padx=10)
    view_stock_button.pack(side=tk.LEFT, padx=10)
    record_stock_button.pack(side=tk.LEFT, padx=10)
    reorder_button.pack(side=tk.LEFT, padx=10)
    product_info_button.pack(side=tk.LEFT, padx=10)

class Customer:
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class SalesHistory:
    def __init__(self):
        self.history = []

    def add_sale(self, customer, product, amount):
        self.history.append((customer, product, amount))

class MarketingCampaigns:
    def __init__(self):
        self.campaigns = []

    def add_campaign(self, inventory_name, discount_sale, campaign_details):
        self.campaigns.append((inventory_name, discount_sale, campaign_details))

class CRMApp:
    def __init__(self, root):
        self.customers = []  # List to store customer objects
        self.sales_history = SalesHistory()
        self.marketing_campaigns = MarketingCampaigns()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        self.add_customer_button = tk.Button(self.main_frame, text="Add Customer", command=self.show_add_customer_window)
        self.display_customer_button = tk.Button(self.main_frame, text="Display Customer", command=self.show_display_customer_window)
        self.sales_history_button = tk.Button(self.main_frame, text="Sales History", command=self.show_sales_history_window)
        self.add_campaign_button = tk.Button(self.main_frame, text="Add Campaign", command=self.show_add_campaign_window)

        self.add_customer_button.grid(row=0, column=0, pady=5)
        self.display_customer_button.grid(row=1, column=0, pady=5)
        self.sales_history_button.grid(row=2, column=0, pady=5)
        self.add_campaign_button.grid(row=3, column=0, pady=5)

    def show_add_customer_window(self):
        self.add_customer_window = tk.Toplevel()
        self.add_customer_window.title("Add Customer")

        self.name_label = tk.Label(self.add_customer_window, text="Name")
        self.email_label = tk.Label(self.add_customer_window, text="Email")
        self.phone_label = tk.Label(self.add_customer_window, text="Phone")
        self.address_label = tk.Label(self.add_customer_window, text="Address")

        self.name_entry = tk.Entry(self.add_customer_window, width=30)
        self.email_entry = tk.Entry(self.add_customer_window, width=30)
        self.phone_entry = tk.Entry(self.add_customer_window, width=30)
        self.address_entry = tk.Entry(self.add_customer_window, width=30)

        self.add_customer_button = tk.Button(self.add_customer_window, text="Add Customer", command=self.add_customer)

        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.email_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.phone_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.address_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_customer_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def add_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if not name or not email or not phone or not address:
            tk.messagebox.showerror("Error", "All fields are required!")
            return

        customer = Customer(name, email, phone, address)
        self.customers.append(customer)

        print(f"Added customer: {name}, Email: {email}, Phone: {phone}, Address: {address}")

        self.add_customer_window.destroy()  # Close the "Add Customer" window after saving

    def show_display_customer_window(self):
        self.display_customer_window = tk.Toplevel()
        self.display_customer_window.title("Display Customer")

        self.name_label = tk.Label(self.display_customer_window, text="Customer Name")
        self.name_entry = tk.Entry(self.display_customer_window, width=30)
        self.display_button = tk.Button(self.display_customer_window, text="Display", command=self.display_customer)

        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.display_button.grid(row=1, column=0, columnspan=2, pady=5)

    def display_customer(self):
        name = self.name_entry.get()

        if not name:
            tk.messagebox.showerror("Error", "Please enter a customer name!")
            return

        found = False
        for customer in self.customers:
            if customer.name == name:
                found = True
                tk.messagebox.showinfo("Customer Information", f"Name: {customer.name}\nEmail: {customer.email}\nPhone: {customer.phone}\nAddress: {customer.address}")
                break

        if not found:
            tk.messagebox.showerror("Error", f"No customer found with the name '{name}'")
    def show_add_campaign_window(self):
        self.add_campaign_window = tk.Toplevel()
        self.add_campaign_window.title("Add Campaign")

        self.inventory_label = tk.Label(self.add_campaign_window, text="Inventory Name")
        self.discount_label = tk.Label(self.add_campaign_window, text="Discount Sale")
        self.campaign_detail_label = tk.Label(self.add_campaign_window, text="Campaign Detail")

        self.inventory_options = ["Item A", "Item B", "Item C"]  # Replace with actual inventory options
        self.discount_options = ["10%", "20%", "30%"]  # Replace with actual discount options
        self.campaign_detail_options = ["Winter Sale", "Spring Sale", "Summer Sale"]  # Replace with actual campaign detail options

        self.inventory_var = tk.StringVar(self.add_campaign_window)
        self.discount_var = tk.StringVar(self.add_campaign_window)
        self.campaign_detail_var = tk.StringVar(self.add_campaign_window)

        self.inventory_var.set(self.inventory_options[0])
        self.discount_var.set(self.discount_options[0])
        self.campaign_detail_var.set(self.campaign_detail_options[0])

        self.inventory_menu = tk.OptionMenu(self.add_campaign_window, self.inventory_var, *self.inventory_options)
        self.discount_menu = tk.OptionMenu(self.add_campaign_window, self.discount_var, *self.discount_options)
        self.campaign_detail_menu = tk.OptionMenu(self.add_campaign_window, self.campaign_detail_var, *self.campaign_detail_options)

        self.add_campaign_button = tk.Button(self.add_campaign_window, text="Add Campaign", command=self.add_campaign)

        self.inventory_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.discount_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.campaign_detail_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.inventory_menu.grid(row=0, column=1, padx=10, pady=5)
        self.discount_menu.grid(row=1, column=1, padx=10, pady=5)
        self.campaign_detail_menu.grid(row=2, column=1, padx=10, pady=5)

        self.add_campaign_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def show_sales_history_window(self):
        self.sales_history_window = tk.Toplevel()
        self.sales_history_window.title("Sales History")

    def add_campaign(self):
        inventory_name = self.inventory_var.get()
        discount_sale = self.discount_var.get()
        campaign_details = self.campaign_detail_var.get()

        self.marketing_campaigns.add_campaign(inventory_name, discount_sale, campaign_details)
        print(f"Added campaign: {campaign_details} with {discount_sale} off on {inventory_name}")

def open_crm():
    crm_window = tk.Toplevel(root)
    crm_window.title("Customer Relationship Management")

    crm_app = CRMApp(crm_window)


if __name__ == "__main__":
    inventory = InventoryManager()

    root = tk.Tk()
    root.title("Main Menu")
    root.title("Financial Management System")

    def open_financial_management():
        app = Application()
        app.mainloop()

        

    financial_button = tk.Button(root, text="Financial Management", command=open_financial_management)
    financial_button.pack(pady=20)

    employee_button = tk.Button(root, text="Employee Management", command=open_employee_management)
    employee_button.pack(pady=20)

    # Create a button for Inventory Management
    inventory_button = tk.Button(root, text="Inventory Management", command=open_inventory_management)
    inventory_button.pack(pady=20)

    # Create a button for Customer Relationship Management
    crm_button = tk.Button(root, text="Customer Relationship Management", command=open_crm)
    crm_button.pack(pady=20)

    root.mainloop()
