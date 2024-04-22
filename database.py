import sqlite3
conn = sqlite3.connect('database.db')

# Create tables
conn.execute('''CREATE TABLE users 
  (userId INTEGER PRIMARY KEY, 
  fullName TEXT,
  email TEXT,
  password TEXT,
  phone TEXT,
  age INTEGER,
  address TEXT
  )''')

conn.execute('''CREATE TABLE products
  (productId INTEGER PRIMARY KEY,
  name TEXT,
  price REAL,
  description TEXT,
  image TEXT,
  stock INTEGER
  )''')

conn.execute('''CREATE TABLE cart
  (userId INTEGER,
  productId INTEGER,
  FOREIGN KEY(userId) REFERENCES users(userId),
  FOREIGN KEY(productId) REFERENCES products(productId)
  )''')


# Insert data into products table
conn.execute('''INSERT INTO products (productId, name, price, description, image, stock) 
                VALUES (1, 'Hoodie', 39.99, 'Stay cozy and stylish with our PSU Hoodie. Made from soft and comfortable fabric.', 'PSU_Hoodie.jpg', 100)''')

conn.execute('''INSERT INTO products (productId, name, price, description, image, stock) 
                VALUES (2, 'T-shirt', 24.99, 'Show off your PSU spirit with our classic T-shirt. Crafted from high-quality cotton.', 'PSU_Shirt.jpg', 150)''')

conn.execute('''INSERT INTO products (productId, name, price, description, image, stock) 
                VALUES (3, 'Water Bottle', 19.99, "Stay hydrated with the PSU water bottle. It's a durable and reusable bottle, perfect for carrying.", 'PSU_Water_bottle.jpg', 200)''')

conn.execute('''INSERT INTO products (productId, name, price, description, image, stock) 
                VALUES (4, 'Backpack', 44.99, 'The PSU backpack is the ultimate accessory for students on the go. It has spacious compartments.', 'PSU_Backpack.png', 80)''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()