from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, static_url_path='/static')
DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Ambarlar tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Malzeme tablosu
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

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template("index.html")

# 🔹 Ambar işlemleri
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM warehouses")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": row[0], "name": row[1]} for row in rows])

@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO warehouses (name) VALUES (?)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ambar eklendi"})

# 🔹 Malzeme işlemleri
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
        data['name'],
        data['unit'],
        data['stock_amount'],
        data.get('cycle_time'),
        data['type'],
        data['warehouse'],
        data['stock_code']
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Malzeme eklendi"})

@app.route('/materials/<int:material_id>', methods=['PUT'])
def update_material(material_id):
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE materials SET
            name = ?, unit = ?, stock_amount = ?, cycle_time = ?, type = ?, warehouse = ?, stock_code = ?
        WHERE id = ?
    ''', (
        data['name'],
        data['unit'],
        data['stock_amount'],
        data.get('cycle_time'),
        data['type'],
        data['warehouse'],
        data['stock_code'],
        material_id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Malzeme güncellendi"})

if __name__ == '__main__':
    app.run(debug=True)
