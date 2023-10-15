import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Product:
    def __init__(self, name, price, quantity, supplier):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier
        self.purchased_quantity = 0
        self.sold_quantity = 0

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

    def reordering(self):
        for product in self.products:
            if product.quantity <= product.reorder_level:
                print(f"Reorder {product.name}, Current Quantity: {product.quantity}")

def open_add_stock_window():
    add_stock_window = tk.Toplevel(root)
    add_stock_window.title("Add Stock")

    # Define a validation function to check if the fields are filled
    def validate_fields():
        required_fields = [(name_entry, "Product Name"), (price_entry, "Price"), (quantity_entry, "Initial Quantity"), (supplier_entry, "Supplier")]
        for entry, label_text in required_fields:
            if not entry.get():
                messagebox.showerror("Error", f"{label_text} is required.")
                return False
        return True

    def add_stock(name_entry, price_entry, quantity_entry, supplier_entry):
        if not validate_fields():  # Check if all fields are filled
            return

        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        supplier = supplier_entry.get()

        product = Product(name, price, quantity, supplier)
        inventory.add_product(product)

        # Clear the entry fields after adding stock
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        supplier_entry.delete(0, tk.END)

        update_listbox()

    # Add red stars to indicate required fields
    required_label = tk.Label(add_stock_window, text="* Required Field", fg="red")
    required_label.grid(row=0, column=2, sticky="w")

    name_label = tk.Label(add_stock_window, text="Product Name")
    price_label = tk.Label(add_stock_window, text="Price")
    quantity_label = tk.Label(add_stock_window, text="Initial Quantity")
    supplier_label = tk.Label(add_stock_window, text="Supplier")

    name_entry = tk.Entry(add_stock_window)
    price_entry = tk.Entry(add_stock_window)
    quantity_entry = tk.Entry(add_stock_window)
    supplier_entry = tk.Entry(add_stock_window)

    add_button = tk.Button(add_stock_window, text="Add Stock", command=lambda: add_stock(name_entry, price_entry, quantity_entry, supplier_entry))

    name_label.grid(row=0, column=0)
    price_label.grid(row=1, column=0)
    quantity_label.grid(row=2, column=0)
    supplier_label.grid(row=3, column=0)

    name_entry.grid(row=0, column=1)
    price_entry.grid(row=1, column=1)
    quantity_entry.grid(row=2, column=1)
    supplier_entry.grid(row=3, column=1)

    add_button.grid(row=4, column=0, columnspan=2, pady=10)

def add_stock(name_entry, price_entry, quantity_entry, supplier_entry):
    name = name_entry.get()
    price = float(price_entry.get())
    quantity = int(quantity_entry.get())
    supplier = supplier_entry.get()

    product = Product(name, price, quantity, supplier)
    inventory.add_product(product)

    update_listbox()

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
            result_label.config(text=f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Supplier: {product.supplier}")
        else:
            result_label.config(text=f"No stock or product found with the name '{name}'")


    view_button = tk.Button(view_stock_window, text="View Product", command=view_product)
    result_label = tk.Label(view_stock_window, text="", font=('Arial', 12))

    view_button.pack(pady=10)
    result_label.pack(pady=10)

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


def open_reorder_window():
    reorder_window = tk.Toplevel(root)
    reorder_window.title("Reorder")

    inventory_list = inventory.view_stock()

    def reorder_product(product_name, quantity):
        for product in inventory.products:
            if product.name == product_name:
                product.quantity += quantity
                print(f"Reordered {product.name}, New Quantity: {product.quantity}")
                reorder_window.destroy()  # Close the reorder window after reordering
                update_listbox()
                return
        else:
            print(f"Product '{product_name}' not found")

    name_label = tk.Label(reorder_window, text="Product Name")
    name_entry = tk.Entry(reorder_window)
    name_label.pack(pady=5)
    name_entry.pack(pady=5)

    quantity_label = tk.Label(reorder_window, text="Reorder Quantity")
    quantity_entry = tk.Entry(reorder_window)
    quantity_label.pack(pady=5)
    quantity_entry.pack(pady=5)

    reorder_button = tk.Button(reorder_window, text="Reorder", command=lambda: reorder_product(name_entry.get(), int(quantity_entry.get())))
    reorder_button.pack(pady=10)

    reorder_window.mainloop()

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

inventory = InventoryManager()

root = tk.Tk()
root.title("Inventory Management")


add_stock_button = tk.Button(root, text="Add Stock", command=open_add_stock_window)
view_stock_button = tk.Button(root, text="View Stock", command=update_listbox)
record_stock_button = tk.Button(root, text="Record Stock", command=open_record_stock_window)
reorder_button = tk.Button(root, text="Reordering", command=open_reorder_window)
product_info_button = tk.Button(root, text="Product Information", command=open_product_info_window)


add_stock_button.pack(side=tk.LEFT, padx=10)
view_stock_button.pack(side=tk.LEFT, padx=10)
record_stock_button.pack(side=tk.LEFT, padx=10)
reorder_button.pack(side=tk.LEFT, padx=10)
product_info_button.pack(side=tk.LEFT, padx=10)

root.mainloop()

