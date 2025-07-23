from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__, static_url_path='/static')

# PostgreSQL bağlantısı (Render için ortam değişkeninden)
DATABASE_URL = os.environ.get("postgresql://poler_postgresql_enes_user:e1Sfai0NvhmznIh4nmSWMMnGU4wOirUj@dpg-d209tdumcj7s73athnp0-a/poler_postgresql_enes")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template("index.html")

# 🔧 Veritabanı tablolarını oluştur
@app.route('/init-db')
def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS warehouses (
            id SERIAL PRIMARY KEY,
            name TEXT
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            name TEXT,
            unit TEXT,
            stock_amount NUMERIC,
            cycle_time TEXT,
            type TEXT,
            warehouse TEXT,
            stock_code TEXT
        );
        """)

        conn.commit()
        cur.close()
        conn.close()
        return "Veritabanı tabloları oluşturuldu."
    except Exception as e:
        return f"Hata: {e}"

# 📥 Yeni ambar ekle
@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "İsim gerekli"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO warehouses (name) VALUES (%s)", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📤 Ambarları listele
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM warehouses")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        warehouses = [{"id": r[0], "name": r[1]} for r in rows]
        return jsonify(warehouses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Gerekirse materials endpoint'leri de burada

if __name__ == '__main__':
    app.run(debug=True)
