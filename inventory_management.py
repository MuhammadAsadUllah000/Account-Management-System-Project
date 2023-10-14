import tkinter as tk

class Product:
    def __init__(self, name, price, quantity, reorder_level):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.reorder_level = reorder_level

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
                product.quantity += quantity
                print(f"Recorded {quantity} units of {product_name}")
                return
        print(f"Product '{product_name}' not found")

    def reordering(self):
        for product in self.products:
            if product.quantity <= product.reorder_level:
                print(f"Reorder {product.name}, Current Quantity: {product.quantity}")

def open_add_stock_window():
    add_stock_window = tk.Toplevel(root)
    add_stock_window.title("Add Stock")

    name_label = tk.Label(add_stock_window, text="Product Name")
    price_label = tk.Label(add_stock_window, text="Price")
    quantity_label = tk.Label(add_stock_window, text="Initial Quantity")
    reorder_label = tk.Label(add_stock_window, text="Reorder Level")

    name_entry = tk.Entry(add_stock_window)
    price_entry = tk.Entry(add_stock_window)
    quantity_entry = tk.Entry(add_stock_window)
    reorder_entry = tk.Entry(add_stock_window)

    add_button = tk.Button(add_stock_window, text="Add Stock", command=lambda: add_stock(name_entry, price_entry, quantity_entry, reorder_entry))

    name_label.grid(row=0, column=0)
    price_label.grid(row=1, column=0)
    quantity_label.grid(row=2, column=0)
    reorder_label.grid(row=3, column=0)

    name_entry.grid(row=0, column=1)
    price_entry.grid(row=1, column=1)
    quantity_entry.grid(row=2, column=1)
    reorder_entry.grid(row=3, column=1)

    add_button.grid(row=4, column=0, columnspan=2, pady=10)

def add_stock(name_entry, price_entry, quantity_entry, reorder_entry):
    name = name_entry.get()
    price = float(price_entry.get())
    quantity = int(quantity_entry.get())
    reorder_level = int(reorder_entry.get())

    product = Product(name, price, quantity, reorder_level)
    inventory.add_product(product)

    update_listbox()

def open_view_stock_window():
    view_stock_window = tk.Toplevel(root)
    view_stock_window.title("View Stock")

    inventory_list = inventory.view_stock()

    listbox = tk.Listbox(view_stock_window, width=60)
    for product in inventory_list:
        listbox.insert(tk.END, f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Reorder Level: {product.reorder_level}")

    listbox.pack(pady=10)

def open_record_stock_window():
    record_stock_window = tk.Toplevel(root)
    record_stock_window.title("Record Stock")

    name_label = tk.Label(record_stock_window, text="Product Name")
    quantity_label = tk.Label(record_stock_window, text="Quantity")

    name_entry = tk.Entry(record_stock_window)
    quantity_entry = tk.Entry(record_stock_window)

    record_button = tk.Button(record_stock_window, text="Record Stock", command=lambda: record_stock(name_entry, quantity_entry))

    name_label.grid(row=0, column=0)
    quantity_label.grid(row=1, column=0)

    name_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)

    record_button.grid(row=2, column=0, columnspan=2, pady=10)

def record_stock(name_entry, quantity_entry):
    name = name_entry.get()
    quantity = int(quantity_entry.get())
    inventory.record_stock(name, quantity)

def open_reorder_window():
    reorder_window = tk.Toplevel(root)
    reorder_window.title("Reorder")

    inventory_list = inventory.view_stock()

    for product in inventory_list:
        if product.quantity <= product.reorder_level:
            label = tk.Label(reorder_window, text=f"Reorder {product.name}, Current Quantity: {product.quantity}")
            label.pack()

def open_product_info_window():
    product_info_window = tk.Toplevel(root)
    product_info_window.title("Product Information")

    name_label = tk.Label(product_info_window, text="Product Name")
    name_entry = tk.Entry(product_info_window)
    name_entry.pack(pady=10)

    info_button = tk.Button(product_info_window, text="Get Product Information", command=lambda: product_info(name_entry.get()))
    info_button.pack(pady=10)

def product_info(name):
    for product in inventory.products:
        if product.name == name:
            print(f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Reorder Level: {product.reorder_level}")
            return
    else:
        print(f"Product '{name}' not found")

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
