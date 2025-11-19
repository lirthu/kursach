import sqlite3
import hashlib

connect = sqlite3.connect('database.db')
c = connect.cursor()
c.execute("PRAGMA foreign_keys = ON;") # подключает внешние ключи (чтобы  можно было делать связи между таблицами)
c.row_factory = sqlite3.Row
c.execute('''
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) UNIQUE NOT NULL ,
    description TEXT NOT NULL)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name VARCHAR(40) NOT NULL,
    brand VARCHAR(20),
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image_path TEXT,
    FOREIGN KEY (category_id) REFERENCES category (id))
''')
c.execute('''
CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    third_name VARCHAR(100),
    login VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    address TEXT NOT NULL,
    role TEXT CHECK(role IN ('user', 'employee')) DEFAULT 'user')
''')
c.execute('''
CREATE TABLE IF NOT EXISTS user_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK(status IN('Оформлен', 'Доставляется', 'Выполнен', 'Отменен')) DEFAULT 'Оформлен',
    sum DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id))
''')
c.execute('''
CREATE TABLE IF NOT EXISTS order_position (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_time DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES user_order (id),
    FOREIGN KEY (product_id) REFERENCES product (id))
''')
c.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES user (id))
''')
c.execute('''
CREATE TABLE IF NOT EXISTS cart_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (cart_id) REFERENCES cart (id),
    FOREIGN KEY (product_id) REFERENCES product (id))
''')

password = hashlib.sha256('1234'.encode()).hexdigest()
c.execute('''INSERT OR IGNORE INTO user (first_name, last_name, third_name, login, password, phone, email, address, role)
             VALUES ('Артём','Баймухомедов','Владиславович','admin',?,'+7 (926) 286-72-45','lirthu777@gmail.com','Moscow','employee')''', (password,))
c.execute('''select * from user''')
res = c.fetchall()
for i in res:
    print(dict(i))
connect.commit()
