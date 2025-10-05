

import datetime
import requests
from flask import jsonify

def query_get_earthquake_data( min_magnitude=2.5, max_magnitude=10.0):


    
    NASA_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    

    params = {
        "minmagnitude": min_magnitude,
        "maxmagnitude": max_magnitude,
    }
    try:
        response = requests.get(NASA_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        # Return only name, place, tsunami, mag, time
        filtered_data = []
        for feature in response.json().get("features", []):
            properties = feature.get("properties", {})
            filtered_data.append({
                "name": properties.get("title"),
                "place": properties.get("place"),
                "tsunami": properties.get("tsunami"),
                "magnitude": properties.get("mag"),
                "time": datetime.datetime.utcfromtimestamp(properties.get("time") / 1000).isoformat() + 'Z' if properties.get("time") else None
            })
        return jsonify(filtered_data)


    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500  


