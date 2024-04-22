from collections import Counter
from flask import Flask, render_template, request, redirect, flash, url_for, session
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = 'SsOMpgU0X#2WX3*(xJ(>'


@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('PSUMerch.html', products=products)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    cart = list()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        generated_hash = hashlib.sha1((password + app.secret_key).encode())
        password = generated_hash.hexdigest()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=? and password=?', (email, password,))
        user = cursor.fetchone()
        if not user:
            flash('Invalid email or password', 'warning')
            conn.close()
        else:
            user_id = user[0]  # userId
            session['loggedin'] = True
            session['id'] = user_id
            session['name'] = user[1]  # fullName
            if 'cart' in session:
                cart = session['cart']
                for product_id in cart:
                    cursor.execute('INSERT INTO cart (userId, productId) VALUES (?, ?)', (user_id, product_id))
                    conn.commit()
            cursor.execute('SELECT productId FROM cart WHERE userId=?', (user_id,))
            products_in_cart = cursor.fetchall()
            cart = [item[0] for item in products_in_cart]
            session['cart'] = cart
            conn.close()
            return redirect(url_for('index'))
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']
        age = request.form['age']
        address = request.form['address']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        user = cursor.fetchone()
        if user:
            flash(f'User with {email} already exists.', 'warning')
            conn.close()
        else:
            generated_hash = hashlib.sha1((password + app.secret_key).encode())
            password = generated_hash.hexdigest()
            cursor.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?)',
                           (name, email, password, phone, age, address))
            conn.commit()
            flash('You have successfully signed up.', 'success')
            # Log in the user automatically after signup
            cursor.execute('SELECT * FROM users WHERE email=?', (email,))
            user = cursor.fetchone()
            session['loggedin'] = True
            session['id'] = user[0]
            session['name'] = user[1]
            conn.close()
            return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    session.pop('cart', None)
    return redirect(url_for('index'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    if 'cart' not in session:
        session['cart'] = list()
    cart = session['cart']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET stock = stock - 1 WHERE productId=?', (product_id,))
    if 'loggedin' in session:
        user_id = session['id']
        cursor.execute('INSERT INTO cart (userId, productId) VALUES (?, ?)', (user_id, product_id))
    conn.commit()
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'loggedin' in session:
        user_id = session['id']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cart WHERE userId = ?', (user_id,))
        conn.commit()
        conn.close()
        session.pop('cart', None)
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = list()
    total = 0
    if 'cart' in session:
        products = session['cart']
        product_counts = Counter(products)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        for product_id, count in product_counts.items():
            cursor.execute('SELECT * FROM products WHERE productId = ?', (product_id,))
            product = cursor.fetchone()
            image = product[4]
            price = product[2]
            name = product[1]
            subtotal = price * count
            total += subtotal
            product_data = product_id, name, price, count, image, subtotal
            cart.append(product_data)
    return render_template('cart.html', cart=cart, total=f'{total:.2f}')


if __name__ == '__main__':
    app.run(debug=True)
