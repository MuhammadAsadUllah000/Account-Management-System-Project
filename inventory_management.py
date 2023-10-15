import tkinter as tk

class Product:
    def __init__(self, name, price, quantity, supplier):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

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
    quantity_label = tk.Label(record_stock_window, text="Quantity")

    name_entry = tk.Entry(record_stock_window)
    quantity_entry = tk.Entry(record_stock_window)

    record_button = tk.Button(record_stock_window, text="Record Stock", command=lambda: record_stock(name_entry, quantity_entry))
    display_button = tk.Button(record_stock_window, text="Display Records", command=lambda: display_records())

    name_label.grid(row=0, column=0)
    quantity_label.grid(row=1, column=0)

    name_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)

    record_button.grid(row=2, column=0, pady=10, padx=5)
    display_button.grid(row=2, column=1, pady=10, padx=5)

def record_stock(name_entry, quantity_entry):
    name = name_entry.get()
    quantity = int(quantity_entry.get())
    inventory.record_stock(name, quantity)
    print(f"Recorded {quantity} units of {name}")

def display_records():
    record_window = tk.Toplevel(root)
    record_window.title("Records")

    inventory_list = inventory.view_stock()

    for product in inventory_list:
        label = tk.Label(record_window, text=f"Name: {product.name}, Quantity: {product.quantity}, Supplier: {product.supplier}")
        label.pack()

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

    info_button = tk.Button(product_info_window, text="Get Product Information", command=lambda: product_info(name_entry.get()))
    info_button.pack(pady=10)

def product_info(name):
    for product in inventory.products:
        if product.name == name:
            print(f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Supplier: {product.supplier}")
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

