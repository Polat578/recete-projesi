from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/warehouses')
def warehouses():
    return render_template("warehouses.html")

@app.route('/materials')
def materials():
    return render_template("materials.html")

if __name__ == '__main__':
    app.run(debug=True)
