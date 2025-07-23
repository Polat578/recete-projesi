from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__, static_url_path='/static')

DATABASE_URL = os.environ.get("DATABASE_URL")
print("🧪 Render ortam değişkeni (DATABASE_URL):", DATABASE_URL)

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL ortam değişkeni tanımlı değil!")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template("index.html")

# ✅ GET materials
@app.route('/materials', methods=['GET'])
def get_materials():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, unit, stock_amount, cycle_time, type, warehouse, stock_code FROM materials")
        rows = cur.fetchall()
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
    except Exception as e:
        print(f"❌ /materials hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500

# ✅ POST materials
@app.route('/materials', methods=['POST'])
def add_material():
    try:
        data = request.get_json()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO materials (name, unit, stock_amount, cycle_time, type, warehouse, stock_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('name'),
            data.get('unit'),
            data.get('stock_amount'),
            data.get('cycle_time'),
            data.get('type'),
            data.get('warehouse'),
            data.get('stock_code')
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "✅ Malzeme eklendi"}), 201
    except Exception as e:
        print(f"❌ Malzeme ekleme hatası: {e}")
        return jsonify({"error": "Malzeme eklenemedi"}), 500

# ✅ GET warehouses
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM warehouses")
        rows = cur.fetchall()
        conn.close()
        return jsonify([
            {"id": row[0], "name": row[1]} for row in rows
        ])
    except Exception as e:
        print(f"❌ /warehouses hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500

# ✅ POST warehouses
@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    try:
        data = request.get_json()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO warehouses (name) VALUES (%s)", (data.get('name'),))
        conn.commit()
        conn.close()
        return jsonify({"message": "✅ Ambar eklendi"}), 201
    except Exception as e:
        print(f"❌ Ambar ekleme hatası: {e}")
        return jsonify({"error": "Ambar eklenemedi"}), 500

# ✅ GET products
@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, unit, stock_amount FROM products")
        rows = cur.fetchall()
        conn.close()
        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "unit": row[2],
                "stock_amount": row[3]
            } for row in rows
        ])
    except Exception as e:
        print(f"❌ /products hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500

# ✅ GET orders
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, product_id, quantity, status FROM orders")
        rows = cur.fetchall()
        conn.close()
        return jsonify([
            {
                "id": row[0],
                "product_id": row[1],
                "quantity": row[2],
                "status": row[3]
            } for row in rows
        ])
    except Exception as e:
        print(f"❌ /orders hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500

# ✅ INIT DB – tüm tabloları oluşturur
@app.route('/init-db')
def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                stock_amount REAL DEFAULT 0,
                cycle_time TEXT,
                type TEXT,
                warehouse TEXT,
                stock_code TEXT
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                stock_amount REAL DEFAULT 0
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS warehouses (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                product_id INTEGER,
                quantity REAL,
                status TEXT
            );
        """)

        conn.commit()
        conn.close()
        return "✅ Veritabanı başarıyla oluşturuldu."
    except Exception as e:
        print(f"❌ init-db hatası: {e}")
        return f"Hata: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
