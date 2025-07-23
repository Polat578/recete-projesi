from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__, static_url_path='/static')

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template("index.html")

# 🔹 GET warehouses
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM warehouses")
        rows = cur.fetchall()
        conn.close()
        return jsonify([{"id": row[0], "name": row[1]} for row in rows])
    except Exception as e:
        print(f"❌ /warehouses GET hatası: {e}")
        return jsonify({"error": "Bir hata oluştu"}), 500

# 🔹 POST warehouses
@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    try:
        data = request.get_json()
        print("📥 Gelen veri:", data)
        if not data or not data.get("name"):
            return jsonify({"error": "İsim boş olamaz"}), 400
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO warehouses (name) VALUES (%s)", (data["name"],))
        conn.commit()
        conn.close()
        return jsonify({"message": "✅ Ambar eklendi"}), 201
    except Exception as e:
        print(f"❌ /warehouses POST hatası: {e}")
        return jsonify({"error": "Ambar eklenemedi"}), 500
