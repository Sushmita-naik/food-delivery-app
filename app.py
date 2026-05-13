from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
# CART
cart = []
# HOME PAGE
@app.route('/')
def home():
    return redirect('/login')
# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('food_ordering.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Customers
        WHERE email=? AND password=?
        """, (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect('/dashboard')
        else:
            message = "Wrong Email or Password"
    return render_template(
        'login.html',
        message=message
    )
# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']
        try:
            conn = sqlite3.connect('food_ordering.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO Customers
            (name, email, phone, password, address)
            VALUES (?, ?, ?, ?, ?)
            """, (name, email, phone, password, address))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        except:
            message = "Email Already Exists"
    return render_template(
        'register.html',
        message=message
    )
# FORGOT PASSWORD
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        conn = sqlite3.connect('food_ordering.db')
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE Customers
        SET password=?
        WHERE email=?
        """, (new_password, email))
        conn.commit()
        conn.close()
        message = "Password Updated Successfully"
    return render_template(
        'forgot_password.html',
        message=message
    )
# DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
# SEARCH FOOD
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('food_ordering.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM FoodItems
    WHERE food_name LIKE ?
    """, ('%' + query + '%',))
    food_items = cursor.fetchall()
    conn.close()
    return render_template(
        'menu.html',
        food_items=food_items
    )
# CATEGORY FILTER
@app.route('/category/<category_name>')
def category(category_name):
    conn = sqlite3.connect('food_ordering.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM FoodItems
    WHERE category = ?
    """, (category_name,))
    food_items = cursor.fetchall()
    conn.close()
    return render_template(
        'menu.html',
        food_items=food_items
    )
# RESTAURANTS PAGE
@app.route('/restaurants')
def restaurants():
    conn = sqlite3.connect('food_ordering.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM Restaurants
    """)
    restaurants = cursor.fetchall()
    conn.close()
    return render_template(
        'restaurants.html',
        restaurants=restaurants
    )
# FOOD MENU PAGE
@app.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    conn = sqlite3.connect('food_ordering.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM FoodItems
    WHERE restaurant_id = ?
    """, (restaurant_id,))
    food_items = cursor.fetchall()
    conn.close()
    return render_template(
        'menu.html',
        food_items=food_items
    )
# ADD TO CART
@app.route('/add_to_cart/<int:food_id>')
def add_to_cart(food_id):
    conn = sqlite3.connect('food_ordering.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM FoodItems
    WHERE food_id = ?
    """, (food_id,))
    item = cursor.fetchone()
    conn.close()
    cart.append(item)
    return redirect('/cart')
# CART PAGE
@app.route('/cart')
def cart_page():
    total = 0
    for item in cart:
        total += item[3]
    return render_template(
        'cart.html',
        cart=cart,
        total=total
    )
# REMOVE FROM CART
@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    if index < len(cart):
        cart.pop(index)
    return redirect('/cart')
# PAYMENT PAGE
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    total = 0
    for item in cart:
        total += item[3]
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        conn = sqlite3.connect('food_ordering.db')
        cursor = conn.cursor()
        # SAVE ORDERS INTO DATABASE
        for item in cart:
            cursor.execute("""
            INSERT INTO Orders
            (food_name, price, payment_method)
            VALUES (?, ?, ?)
            """, (
                item[2],
                item[3],
                payment_method

            ))
        conn.commit()
        conn.close()
        return render_template(
            'receipt.html',
            cart=cart,
            total=total,
            payment_method=payment_method
        )
    return render_template(
        'payment.html',
        total=total
    )
# PLACE ORDER
@app.route('/place_order')
def place_order():
    return redirect('/payment')
# SUCCESS PAGE
@app.route('/success')
def success():
    return render_template('success.html')
# LOGOUT
@app.route('/logout')
def logout():
    return redirect('/login')
# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
