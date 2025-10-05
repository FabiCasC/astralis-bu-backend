

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


# {
# "bbox": [
# -179.4936,
# -35.5811,
# -0.37,
# 179.0068,
# 71.2917,
# 643.06
# ],
# "features": [
# {
# "geometry": {
# "coordinates": [
# -102.073,
# 32.441,
# 4.3872
# ],
# "type": "Point"
# },
# "id": "tx2025tqakuj",
# "properties": {
# "alert": null,
# "cdi": null,
# "code": "2025tqakuj",
# "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/tx2025tqakuj.geojson",
# "dmin": 0,
# "felt": null,
# "gap": 143,
# "ids": ",tx2025tqakuj,",
# "mag": 1.4,
# "magType": "ml",
# "mmi": null,
# "net": "tx",
# "nst": 31,
# "place": "34 km SSW of Los Ybanez, Texas",
# "rms": 0.5,
# "sig": 30,
# "sources": ",tx,",
# "status": "automatic",
# "time": 1759695299925,
# "title": "M 1.4 - 34 km SSW of Los Ybanez, Texas",
# "tsunami": 0,
# "type": "earthquake",
# "types": ",origin,phase-data,",
# "tz": null,
# "updated": 1759695475519,
# "url": "https://earthquake.usgs.gov/earthquakes/eventpage/tx2025tqakuj"
# },
# "type": "Feature"
# },
# {
# "geometry": {
# "coordinates": [
# -119.8458,
# 39.6607,
# 4.1
# ],
# "type": "Point"
# },
# "id": "nn00905479",
# "properties": {
# "alert": null,
# "cdi": null,
# "code": "00905479",
# "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/nn00905479.geojson",
# "dmin": 0.081,
# "felt": null,
# "gap": 80.27000000000001,
# "ids": ",nn00905479,",
# "mag": 1,
# "magType": "ml",
# "mmi": null,
# "net": "nn",
# "nst": 10,
# "place": "2 km N of Lemmon Valley, Nevada",
# "rms": 0.0609,
# "sig": 15,
# "sources": ",nn,",
# "status": "automatic",
# "time": 1759694898374,
# "title": "M 1.0 - 2 km N of Lemmon Valley, Nevada",
# "tsunami": 0,
# "type": "earthquake",
# "types": ",origin,phase-data,",