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
        for product in self.products:
            print(f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Reorder Level: {product.reorder_level}")

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

def display_menu():
    print("\nMenu:")
    print("1. Add Stock")
    print("2. View Stock")
    print("3. Record Stock")
    print("4. Reordering")
    print("5. Product Information")
    print("6. Quit")

def main():
    inventory = InventoryManager()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter initial quantity: "))
            reorder_level = int(input("Enter reorder level: "))

            product = Product(name, price, quantity, reorder_level)
            inventory.add_product(product)

        elif choice == '2':
            inventory.view_stock()

        elif choice == '3':
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity to record: "))
            inventory.record_stock(name, quantity)

        elif choice == '4':
            inventory.reordering()

        elif choice == '5':
            name = input("Enter product name: ")
            for product in inventory.products:
                if product.name == name:
                    print(f"Name: {product.name}, Price: ${product.price}, Quantity: {product.quantity}, Reorder Level: {product.reorder_level}")
                    break
            else:
                print(f"Product '{name}' not found")

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
