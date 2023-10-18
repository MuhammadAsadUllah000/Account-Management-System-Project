import tkinter as tk

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
        self.display_customers_button = tk.Button(self.main_frame, text="Display Customers", command=self.display_customers)
        self.add_sale_button = tk.Button(self.main_frame, text="Add Sale", command=self.add_sale)
        self.add_campaign_button = tk.Button(self.main_frame, text="Add Campaign", command=self.add_campaign)

        self.add_customer_button.grid(row=0, column=0, pady=5)
        self.display_customers_button.grid(row=1, column=0, pady=5)
        self.add_sale_button.grid(row=2, column=0, pady=5)
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

        customer = Customer(name, email, phone, address)
        self.customers.append(customer)

        print(f"Added customer: {name}, Email: {email}, Phone: {phone}, Address: {address}")

        self.add_customer_window.destroy()  # Close the "Add Customer" window after saving

    def display_customers(self):
        display_window = tk.Toplevel()
        display_window.title("Customer Information")

        for customer in self.customers:
            tk.Label(display_window, text=f"Name: {customer.name}").pack()
            tk.Label(display_window, text=f"Email: {customer.email}").pack()
            tk.Label(display_window, text=f"Phone: {customer.phone}").pack()
            tk.Label(display_window, text=f"Address: {customer.address}").pack()
            tk.Label(display_window, text="-------------------------").pack()

    def add_sale(self):
        # Add code to retrieve customer, product, and amount
        customer = self.customers[0]  # Example: Using the first customer for simplicity
        product = "Product A"  # Example: Replace with actual product selection
        amount = 100  # Example: Replace with actual amount

        self.sales_history.add_sale(customer, product, amount)
        print(f"Added sale: {customer.name} purchased {product} for {amount} USD")

    def add_campaign(self):
        # Add code to retrieve inventory name, discount sale, and campaign details
        inventory_name = "Inventory X"  # Example: Replace with actual inventory selection
        discount_sale = 0.2  # Example: Replace with actual discount
        campaign_details = "Summer Sale"  # Example: Replace with actual campaign details

        self.marketing_campaigns.add_campaign(inventory_name, discount_sale, campaign_details)
        print(f"Added campaign: {campaign_details} with {discount_sale*100}% off on {inventory_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRMApp(root)
    root.mainloop()
