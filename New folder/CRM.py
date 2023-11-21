import tkinter as tk
from tkinter import messagebox 

class Customer:
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.remaining_quantity = quantity

    def sell(self, amount):
        self.remaining_quantity -= amount

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, name, price, quantity):
        product = Product(name, price, quantity)
        self.products.append(product)

class MarketingCampaigns:
    def __init__(self):
        self.campaigns = []

    def add_campaign(self, inventory_name, discount_sale, campaign_details):
        self.campaigns.append((inventory_name, discount_sale, campaign_details))

class CRMApp:
    def __init__(self, root):
        self.customers = []  # List to store customer objects
        self.inventory = InventoryManager()
        self.marketing_campaigns = MarketingCampaigns()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        # Buttons to perform different actions
        self.add_customer_button = tk.Button(self.main_frame, text="Add Customer", command=self.show_add_customer_window)
        self.display_customer_button = tk.Button(self.main_frame, text="Display Customer", command=self.show_display_customer_window)
        self.add_campaign_button = tk.Button(self.main_frame, text="Add Campaign", command=self.show_add_campaign_window)

        # Grid layout for buttons
        self.add_customer_button.grid(row=0, column=0, pady=5)
        self.display_customer_button.grid(row=1, column=0, pady=5)
        self.add_campaign_button.grid(row=2, column=0, pady=5)

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

        self.inventory_options = ["Inventory A", "Inventory B", "Inventory C"]  # Replace with actual inventory options
        self.discount_options = ["Up to 30% Off", "Up to 50% Off", "Up to 70% Off"]  # Replace with actual discount options
        self.campaign_detail_options = ["Clearance Sale", "Cyber Monday sale", "11.11 Sale"]  # Replace with actual campaign detail options

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

    def add_campaign(self):
        inventory_name = self.inventory_var.get()
        discount_sale = self.discount_var.get()
        campaign_details = self.campaign_detail_var.get()

        # Add campaign logic here

if __name__ == "__main__":
    root = tk.Tk()
    app = CRMApp(root)
    root.mainloop()
