from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def login():
    return jsonify({"message": "Ruta de login activa ✅"})
