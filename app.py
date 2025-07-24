from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Ana Sayfa
@app.route('/')
def index():
    return render_template("index.html")

# Ambar Sayfası
@app.route('/warehouses')
def warehouses():
    return render_template("warehouses.html")

# Malzeme Sayfası (Firebase ile çalışır)
@app.route('/materials')
def materials():
    return render_template("materials.html")

# Eğer başka sayfalar da varsa burada eklenebilir

if __name__ == '__main__':
    app.run(debug=True)
