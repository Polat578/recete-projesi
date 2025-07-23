from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

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
    return render_template("index.html")

@app.route('/materials', methods=['GET'])
def get_materials():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, unit, stock_amount, cycle_time, type, warehouse, stock_code FROM materials")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {
            "name": row[0],
            "unit": row[1],
            "stock_amount": row[2],
            "cycle_time": row[3],
            "type": row[4],
            "warehouse": row[5],
            "stock_code": row[6]
        }
        for row in rows
    ])

@app.route('/materials', methods=['POST'])
def add_material():
    data = request.get_json()
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

@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name FROM warehouses")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"name": row[0]} for row in rows])

@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO warehouses (name) VALUES (?)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ambar eklendi."})

if __name__ == '__main__':
    app.run(debug=True)
