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
            stock_amount REAL DEFAULT 0,
            cycle_time TEXT,
            type TEXT,
            warehouse TEXT,
            stock_code TEXT
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

    c.execute('''
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

# --- Malzemeler ---
@app.route('/materials', methods=['GET'])
def get_materials():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM materials")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "unit": row[2],
            "stock_amount": row[3],
            "cycle_time": row[4],
            "type": row[5],
            "warehouse": row[6],
            "stock_code": row[7]
        } for row in rows
    ])

@app.route('/materials', methods=['POST'])
def add_material():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO materials (name, unit, stock_amount, cycle_time, type, warehouse, stock_code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('unit'),
        data.get('stock_amount', 0),
        data.get('cycle_time'),
        data.get('type'),
        data.get('warehouse'),
        data.get('stock_code')
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Malzeme eklendi."})

# --- Ürünler ---
@app.route('/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (name) VALUES (?)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ürün eklendi."})

# --- Reçeteler ---
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
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

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
    return jsonify([{"material": r[0], "quantity": r[1], "unit": r[2]} for r in rows])

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

# --- Üretim Emirleri ---
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
    return jsonify([{"id": r[0], "product": r[1], "quantity": r[2], "status": r[3]} for r in rows])

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

# --- Ambarlar ---
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM warehouses")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO warehouses (name) VALUES (?)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ambar eklendi."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
