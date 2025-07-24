from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__, static_url_path='/static')

# PostgreSQL bağlantısı
DATABASE_URL = "postgresql://poler_postgresql_enes_user:e1Sfai0NvhmznIh4nmSWMMnGU4wOirUj@dpg-d209tdumcj7s73athnp0-a.oregon-postgres.render.com/poler_postgresql_enes"


def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template("index.html")

# 🔹 Veritabanı Tablolarını Oluştur
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
        return "✅ Veritabanı tabloları oluşturuldu"
    except Exception as e:
        return f"HATA: {e}", 500


# 🔹 AMBAR GET
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM warehouses")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": row[0], "name": row[1]} for row in rows])
    except Exception as e:
        print(f"❌ /warehouses GET hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500


# 🔹 AMBAR POST
@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    try:
        data = request.get_json()
        if not data or not data.get("name"):
            return jsonify({"error": "Geçersiz veri"}), 400

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO warehouses (name) VALUES (%s)", (data["name"],))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Ambar başarıyla eklendi."}), 201
    except Exception as e:
        print(f"❌ /warehouses POST hatası: {e}")
        return jsonify({"error": "Ambar eklenemedi"}), 500


# 🔹 MALZEME GET
@app.route('/materials', methods=['GET'])
def get_materials():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, unit, stock_amount, cycle_time, type, warehouse, stock_code FROM materials")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "name": row[1],
                "unit": row[2],
                "stock_amount": row[3],
                "cycle_time": row[4],
                "type": row[5],
                "warehouse": row[6],
                "stock_code": row[7]
            })
        return jsonify(result)
    except Exception as e:
        print(f"❌ /materials GET hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500


# 🔹 MALZEME POST
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
            data.get("name"),
            data.get("unit"),
            data.get("stock_amount"),
            data.get("cycle_time"),
            data.get("type"),
            data.get("warehouse"),
            data.get("stock_code")
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Malzeme eklendi"}), 201
    except Exception as e:
        print(f"❌ /materials POST hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500


if __name__ == '__main__':
    app.run(debug=True)
