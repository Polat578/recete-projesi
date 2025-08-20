from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/materials")
def materials():
    return render_template("materials.html")

@app.route("/warehouses")
def warehouses():
    return render_template("warehouses.html")

@app.route("/movements")
def movements():
    return render_template("movements.html")
