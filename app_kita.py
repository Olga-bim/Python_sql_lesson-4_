import sqlite3
import enum

# Enum for menu actions
class Actions(enum.Enum):
    ADD_CUSTOMER = 1
    VIEW_CUSTOMERS = 2
    UPDATE_CUSTOMER = 3
    DELETE_CUSTOMER = 4
    ADD_CAR = 5
    VIEW_CARS = 6
    UPDATE_CAR = 7
    DELETE_CAR = 8
    EXIT = 9

# Initialize database and tables
def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE)
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            customer_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers(id))
    ''')
    conn.commit()
    conn.close()

# Display the menu
def display_menu():
    print("Menu:")
    print(f"{Actions.ADD_CUSTOMER.value}. Add Customer")
    print(f"{Actions.VIEW_CUSTOMERS.value}. View Customers")
    print(f"{Actions.UPDATE_CUSTOMER.value}. Update Customer")
    print(f"{Actions.DELETE_CUSTOMER.value}. Delete Customer")
    print(f"{Actions.ADD_CAR.value}. Add Car")
    print(f"{Actions.VIEW_CARS.value}. View Cars")
    print(f"{Actions.UPDATE_CAR.value}. Update Car")
    print(f"{Actions.DELETE_CAR.value}. Delete Car")
    print(f"{Actions.EXIT.value}. Exit")

# CRUD operations for customers
def add_customer():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    print("Customer added.")

def view_customers():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def update_customer():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    customer_id = int(input("Enter customer ID to update: "))
    new_name = input("Enter new name: ")
    new_email = input("Enter new email: ")
    cursor.execute("UPDATE customers SET name = ?, email = ? WHERE id = ?", (new_name, new_email, customer_id))
    conn.commit()
    conn.close()
    print("Customer updated.")

def delete_customer():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    customer_id = int(input("Enter customer ID to delete: "))
    # Ensure no cars are associated with this customer before deleting
    cursor.execute("DELETE FROM cars WHERE customer_id = ?", (customer_id,))
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    print("Customer and associated cars deleted.")

# CRUD operations for cars
def add_car():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    model = input("Enter car model: ")
    year = int(input("Enter car year: "))
    view_customers()
    customer_id = int(input("Enter customer ID for this car: "))
    cursor.execute("INSERT INTO cars (model, year, customer_id) VALUES (?, ?, ?)", (model, year, customer_id))
    conn.commit()
    conn.close()
    print("Car added.")

def view_cars():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cars.id, cars.model, cars.year, customers.name
        FROM cars
        JOIN customers ON cars.customer_id = customers.id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def update_car():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    car_id = int(input("Enter car ID to update: "))
    new_model = input("Enter new model: ")
    new_year = int(input("Enter new year: "))
    view_customers()
    new_customer_id = int(input("Enter new customer ID for this car: "))
    cursor.execute("UPDATE cars SET model = ?, year = ?, customer_id = ? WHERE id = ?", (new_model, new_year, new_customer_id, car_id))
    conn.commit()
    conn.close()
    print("Car updated.")

def delete_car():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    car_id = int(input("Enter car ID to delete: "))
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    print("Car deleted.")

# Main function
def main():
    initialize_db()
    while True:
        display_menu()
        try:
            choice = int(input("Please enter your choice: "))
            if choice == Actions.ADD_CUSTOMER.value:
                add_customer()
            elif choice == Actions.VIEW_CUSTOMERS.value:
                view_customers()
            elif choice == Actions.UPDATE_CUSTOMER.value:
                update_customer()
            elif choice == Actions.DELETE_CUSTOMER.value:
                delete_customer()
            elif choice == Actions.ADD_CAR.value:
                add_car()
            elif choice == Actions.VIEW_CARS.value:
                view_cars()
            elif choice == Actions.UPDATE_CAR.value:
                update_car()
            elif choice == Actions.DELETE_CAR.value:
                delete_car()
            elif choice == Actions.EXIT.value:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
