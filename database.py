import sqlite3


# CONNECT DATABASE

conn = sqlite3.connect('food_ordering.db')

cursor = conn.cursor()

# CUSTOMERS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (

    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT UNIQUE,

    phone TEXT,

    password TEXT,

    address TEXT
)
""")


# RESTAURANTS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS Restaurants (

    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,

    restaurant_name TEXT,

    location TEXT,

    contact TEXT
)
""")

# FOOD ITEMS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS FoodItems (

    food_id INTEGER PRIMARY KEY AUTOINCREMENT,

    restaurant_id INTEGER,

    food_name TEXT,

    price REAL,

    category TEXT
)
""")


# ORDERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (

    order_id INTEGER PRIMARY KEY AUTOINCREMENT,

    food_name TEXT,

    price REAL,

    payment_method TEXT
)
""")


# DELETE OLD DATA
cursor.execute("DELETE FROM Restaurants")
cursor.execute("DELETE FROM FoodItems")


# INSERT RESTAURANTS
restaurants = [

    ('Pizza Palace', 'Mangalore', '9876543210'),

    ('Burger Hub', 'Bangalore', '9988776655'),

    ('Spicy Kitchen', 'Udupi', '9123456780'),

    ('Royal Biryani', 'Mysore', '9012345678'),

    ('South Spice', 'Manipal', '9345678901'),

    ('Chinese Wok', 'Bangalore', '9988123456'),

    ('Cafe Delight', 'Mangalore', '9870011223'),

    ('Tandoori Treats', 'Hubli', '9445566778')

]

cursor.executemany("""
INSERT INTO Restaurants
(restaurant_name, location, contact)

VALUES (?, ?, ?)
""", restaurants)


# INSERT FOOD ITEMS

food_items = [

    # PIZZA PALACE
    (1, 'Veg Pizza', 250, 'Pizza'),
    (1, 'Cheese Pizza', 320, 'Pizza'),
    (1, 'Paneer Pizza', 350, 'Pizza'),
    (1, 'Farmhouse Pizza', 400, 'Pizza'),
    (1, 'Pepperoni Pizza', 450, 'Pizza'),
    (1, 'Garlic Bread', 120, 'Side Dish'),
    (1, 'French Fries', 100, 'Snacks'),
    (1, 'Coke', 50, 'Drinks'),

    # BURGER HUB
    (2, 'Chicken Burger', 180, 'Burger'),
    (2, 'Veg Burger', 150, 'Burger'),
    (2, 'Cheese Burger', 220, 'Burger'),
    (2, 'Double Patty Burger', 280, 'Burger'),
    (2, 'Chicken Wings', 300, 'Snacks'),
    (2, 'Mojito', 90, 'Drinks'),
    (2, 'Cold Coffee', 130, 'Drinks'),

    # SPICY KITCHEN
    (3, 'Chicken Biryani', 250, 'Main Course'),
    (3, 'Veg Biryani', 200, 'Main Course'),
    (3, 'Fried Rice', 170, 'Main Course'),
    (3, 'Noodles', 190, 'Main Course'),
    (3, 'Butter Chicken', 320, 'Main Course'),
    (3, 'Paneer Butter Masala', 280, 'Main Course'),
    (3, 'Tandoori Chicken', 350, 'Starter'),
    (3, 'Ice Cream', 90, 'Dessert'),

    # ROYAL BIRYANI
    (4, 'Hyderabadi Biryani', 320, 'Biryani'),
    (4, 'Mutton Biryani', 420, 'Biryani'),
    (4, 'Chicken Kebabs', 280, 'Starter'),
    (4, 'Raita', 60, 'Side Dish'),
    (4, 'Falooda', 110, 'Dessert'),

    # SOUTH SPICE
    (5, 'Masala Dosa', 90, 'Breakfast'),
    (5, 'Idli Vada', 70, 'Breakfast'),
    (5, 'Poori Bhaji', 85, 'Breakfast'),
    (5, 'Filter Coffee', 40, 'Drinks'),
    (5, 'Mini Meals', 150, 'Lunch'),

    # CHINESE WOK
    (6, 'Chicken Noodles', 220, 'Chinese'),
    (6, 'Veg Fried Rice', 180, 'Chinese'),
    (6, 'Manchurian', 190, 'Starter'),
    (6, 'Spring Rolls', 160, 'Starter'),
    (6, 'Schezwan Rice', 230, 'Chinese'),

    # CAFE DELIGHT
    (7, 'Chocolate Cake', 140, 'Dessert'),
    (7, 'Brownie', 120, 'Dessert'),
    (7, 'Cappuccino', 110, 'Coffee'),
    (7, 'Sandwich', 130, 'Snacks'),
    (7, 'Pasta', 240, 'Italian'),

    # TANDOORI TREATS
    (8, 'Butter Naan', 40, 'Indian Bread'),
    (8, 'Paneer Tikka', 260, 'Starter'),
    (8, 'Chicken Tandoori', 380, 'Starter'),
    (8, 'Dal Fry', 180, 'Main Course'),
    (8, 'Jeera Rice', 140, 'Main Course')

]

cursor.executemany("""
INSERT INTO FoodItems
(restaurant_id, food_name, price, category)

VALUES (?, ?, ?, ?)
""", food_items)


# SAVE DATABASE

conn.commit()

conn.close()

print("Database Created Successfully")
