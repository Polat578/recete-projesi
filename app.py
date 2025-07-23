from flask import Flask, jsonify, render_template
import psycopg2
import os

app = Flask(__name__, static_url_path='/static')

# DATABASE_URL ortam değişkenini oku
DATABASE_URL = os.environ.get("DATABASE_URL")

# 🧪 Test: Ortam değişkeni geliyor mu?
print("🧪 Render ortam değişkeni (DATABASE_URL):", DATABASE_URL)

# Ortam değişkeni tanımlı değilse açık hata ver
if not DATABASE_URL:
    raise RuntimeError("❌ HATA: DATABASE_URL ortam değişkeni tanımlı değil. Render ayarlarını kontrol et.")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template("index.html")

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

# ✅ Geçici: Tabloyu oluşturmak için bir kere çalıştırılacak route
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
        conn.commit()
        conn.close()
        return "✅ Veritabanı başarıyla oluşturuldu."
    except Exception as e:
        print(f"❌ init-db hatası: {e}")
        return f"Hata: {e}", 500
