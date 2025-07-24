from flask import Flask, send_from_directory, render_template

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Ana sayfa (varsa)
@app.route('/')
def index():
    return render_template("index.html")  # Veya send_from_directory() ile değiştirebilirsin

# Firebase tabanlı ambar sayfası
@app.route('/firebase-warehouses')
def firebase_warehouses():
    return send_from_directory(app.static_folder, 'warehouses.html')

if __name__ == '__main__':
    app.run(debug=True)
