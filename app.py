from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template("index.html")  # Ana panel

@app.route('/warehouses')
def warehouses():
    return render_template("warehouses.html")  # Ambar sayfası

if __name__ == '__main__':
    app.run(debug=True)
