import tkinter as tk
import subprocess


def open_account():
    subprocess.Popen(["python", "accounts.py"])

def open_employee():
    subprocess.Popen(["python", "employees.py"])

def open_inventory():
    subprocess.Popen(["python", "inventory.py"])

def open_customer():
    subprocess.Popen(["python", "crm.py"])

root = tk.Tk()
root.title("Management System")
root.geometry("850x250")
root.configure(bg='black')  # Set background color to black

# Function to create and style buttons
def create_button(text, command):
    button = tk.Button(
        root, 
        text=text, 
        command=command, 
        width=20, 
        height=2, 
        font=("Helvetica", 12, 'bold'),  # Set font to Helvetica and bold
        fg='black',  # Set font color to black
        bg='green',  # Set button color to green
        relief=tk.FLAT  # Flat button style
    )
    return button

account_button = tk.Button(root, text="Account Management", command=open_account)

employee_button = tk.Button(root, text="Employee Management", command=open_employee)

inventory_button = tk.Button(root, text="Inventory Management", command=open_inventory)

customer_button = tk.Button(root, text="Customer Management", command=open_customer)

# Applying styles to the buttons
for button in (account_button, employee_button, inventory_button, customer_button):
    button.config(
        font=("Helvetica", 12, 'bold'),
        fg='black',
        bg='beige',
        relief=tk.FLAT,
        width=20,
        height=2
    )

account_button.grid(row=0, column=0, padx=5, pady=100, sticky="nsew")
employee_button.grid(row=0, column=1, padx=5, pady=100, sticky="nsew")
inventory_button.grid(row=0, column=2, padx=5, pady=100, sticky="nsew")
customer_button.grid(row=0, column=3, padx=5, pady=100, sticky="nsew")

# Configure grid weights to center the buttons
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure((0, 1, 2, 3), weight=1)

root.mainloop()
