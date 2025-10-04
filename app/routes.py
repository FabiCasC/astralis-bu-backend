from app import app
from flask import jsonify

@app.route("/")
def home():
    return jsonify({"message": "Hola desde Flask organizado 🚀"})

