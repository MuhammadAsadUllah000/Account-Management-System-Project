import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

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

    # Create a button for Inventory Management
    inventory_button = tk.Button(root, text="Inventory Management", command=open_inventory_management)
    inventory_button.pack(pady=20)

    # Create a button for Customer Relationship Management
    crm_button = tk.Button(root, text="Customer Relationship Management", command=open_crm)
    crm_button.pack(pady=20)

    root.mainloop()
