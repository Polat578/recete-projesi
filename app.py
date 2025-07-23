from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, static_url_path='/static')
DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            stock_amount REAL DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (material_id) REFERENCES materials(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS production_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT DEFAULT 'Üretimde',
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materials', methods=['POST'])
def add_material():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO materials (name, unit, stock_amount) VALUES (?, ?, ?)",
              (data['name'], data['unit'], data.get('stock_amount', 0)))
    conn.commit()
    conn.close()
    return jsonify({"message": "Malzeme eklendi."})

@app.route('/materials', methods=['GET'])
def get_materials():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM materials")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": row[0], "name": row[1], "unit": row[2], "stock_amount": row[3]} for row in rows
    ])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (name) VALUES (?)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ürün eklendi."})

@app.route('/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": row[0], "name": row[1]} for row in rows
    ])

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO recipes (product_id, material_id, quantity) VALUES (?, ?, ?)",
              (data['product_id'], data['material_id'], data['quantity']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Reçeteye eklendi."})

@app.route('/recipes/<int:product_id>', methods=['GET'])
def get_recipe(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT m.name, r.quantity, m.unit
        FROM recipes r
        JOIN materials m ON r.material_id = m.id
        WHERE r.product_id = ?
    ''', (product_id,))
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"material": row[0], "quantity": row[1], "unit": row[2]} for row in rows
    ])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO production_orders (product_id, quantity) VALUES (?, ?)",
              (data['product_id'], data['quantity']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Üretim emri oluşturuldu."})

@app.route('/orders', methods=['GET'])
def list_orders():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT o.id, p.name, o.quantity, o.status
        FROM production_orders o
        JOIN products p ON o.product_id = p.id
    ''')
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": row[0], "product": row[1], "quantity": row[2], "status": row[3]} for row in rows
    ])

@app.route('/orders/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT product_id, quantity FROM production_orders WHERE id = ?", (order_id,))
    order = c.fetchone()
    if not order:
        return jsonify({"error": "Üretim emri bulunamadı"}), 404

    product_id, product_qty = order

    c.execute("SELECT material_id, quantity FROM recipes WHERE product_id = ?", (product_id,))
    recipe_items = c.fetchall()

    for material_id, qty_per_unit in recipe_items:
        total_qty = qty_per_unit * product_qty
        c.execute("UPDATE materials SET stock_amount = stock_amount - ? WHERE id = ?", (total_qty, material_id))

    c.execute("UPDATE production_orders SET status = 'Tamamlandı' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Üretim tamamlandı, stoklar güncellendi."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    @app.route('/recipes', methods=['GET'])
def list_recipes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT r.product_id, p.name
        FROM recipes r
        JOIN products p ON r.product_id = p.id
    ''')
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": row[0], "name": row[1]} for row in rows
    ])

