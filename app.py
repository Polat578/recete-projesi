from flask import Flask, jsonify, render_template
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

# ✅ MATERIALS
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

# ✅ PRODUCTS
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

# ✅ WAREHOUSES
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM warehouses")
        rows = cur.fetchall()
        conn.close()
        return jsonify([
            {
                "id": row[0],
                "name": row[1]
            } for row in rows
        ])
    except Exception as e:
        print(f"❌ /warehouses hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500

# ✅ ORDERS
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

# ✅ INIT DB: Tüm tabloları oluşturur
@app.route('/init-db')
def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        # materials tablosu
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

        # products tablosu
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                stock_amount REAL DEFAULT 0
            );
        """)

        # warehouses tablosu
        cur.execute("""
            CREATE TABLE IF NOT EXISTS warehouses (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)

        # orders tablosu
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

# Render için bu satır şart değil ama yerelde test ediyorsan faydalı
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
