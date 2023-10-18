import tkinter as tk

class Customer:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

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
        self.customers = []
        self.sales_history = SalesHistory()
        self.marketing_campaigns = MarketingCampaigns()

        self.name_entry = tk.Entry(root, width=30)
        self.email_entry = tk.Entry(root, width=30)
        self.phone_entry = tk.Entry(root, width=30)

        self.add_customer_button = tk.Button(root, text="Add Customer", command=self.add_customer)
        self.add_sale_button = tk.Button(root, text="Add Sale", command=self.add_sale)
        self.add_campaign_button = tk.Button(root, text="Add Campaign", command=self.add_campaign)

        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_customer_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)
        self.add_sale_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)
        self.add_campaign_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def add_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        customer = Customer(name, email, phone)
        self.customers.append(customer)

        print(f"Added customer: {name}, Email: {email}, Phone: {phone}")

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
