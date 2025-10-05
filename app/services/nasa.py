import json
from flask import jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
NASA_API_URL = "https://api.nasa.gov/neo/rest/v1"

def query_neo_by_id(neo_id):
    params = {
        "api_key": NASA_API_KEY
    }
    url = f"{NASA_API_URL}/neo/{neo_id}"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

def get_browse_ids():
    params = {
        "api_key": NASA_API_KEY
    }
    url = f"{NASA_API_URL}/neo/browse"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        objects = []
        for obj in response.json()["near_earth_objects"]:
            objects.append({
                "id": obj["id"],
                "name": obj["name"]
            })
        return objects
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500