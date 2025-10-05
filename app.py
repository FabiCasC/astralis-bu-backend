from flask import Flask, request, jsonify
import requests
import os
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.services.trajectory import get_trajectory_by_neoid
from app.services.nasa import query_neo_by_id
import logging

logging.basicConfig(level=logging.INFO, )
load_dotenv()
app = Flask(__name__)

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
NASA_API_URL = "https://api.nasa.gov/neo/rest/v1"


@app.route("/nasa/feed", methods=["GET"])
def get_neo_data():
    """Fetches near-earth object data from NASA API and returns raw JSON."""
    start_date = request.args.get("start_date", (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d"))
    end_date = request.args.get("end_date", datetime.utcnow().strftime("%Y-%m-%d"))
    if not start_date or not end_date:
        return jsonify({"error": "Start and end date are required"}), 400

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY
    }
    url = f"{NASA_API_URL}/feed"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/nasa/neo", methods=["GET"])
def get_neo_data_by_id():
    asteroid_id = request.args.get("asteroid_id")
    if not asteroid_id:
        return jsonify({"error": "Asteroid ID is required"}), 400
    return jsonify(query_neo_by_id(asteroid_id))


@app.route("/nasa/mock_trajectory/<neo_id>", methods=["GET"])
def get_mock_trajectory(neo_id):
    """Returns mock trajectory data for a given NEO ID."""
    np.random.seed(int(neo_id) % 1000)  # deterministic mock
    timestamps = [datetime.utcnow() + timedelta(minutes=i * 10) for i in range(5)]
    trajectory = [
        {
            "timestamp": t.isoformat() + "Z",
            "x": float(np.sin(i / 3) * 0.1),
            "y": float(np.cos(i / 3) * 0.1),
            "z": float(np.sin(i / 5) * 0.05)
        }
        for i, t in enumerate(timestamps)
    ]

    return jsonify({
        "neo_id": neo_id,
        "trajectory": trajectory
    })


import ast
from flask import request, jsonify

@app.route("/nasa/trajectory/<neo_id>", methods=["GET"])
def get_trajectory(neo_id):
    if not neo_id:
        return jsonify({"error": "NEO ID is required"}), 400

    position_str = request.args.get("position_km")
    velocity_str = request.args.get("velocity_kms")
    dt = request.args.get("dt", type=float, default=0.5)
    density = request.args.get("density_kg_m3", type=float)

    try:
        position_km = ast.literal_eval(position_str)
        velocity_kms = ast.literal_eval(velocity_str)
    except Exception:
        return jsonify({"error": "Invalid position or velocity format"}), 400

    return jsonify(
        get_trajectory_by_neoid(
            neo_id,
            position_km,
            velocity_kms,
            density,
            dt
        )
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
