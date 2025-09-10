import os
import requests
from dotenv import load_dotenv
from src.utils.retry import call_api_with_retries

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def places_api(query="restaurant", country="us", lat="40.7128", lng="-74.0060"):
    """Call RapidAPI Maps API with retries"""
    url = "https://maps-data.p.rapidapi.com/searchmaps.php"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "maps-data.p.rapidapi.com"
    }
    params = {
        "query": query,
        "limit": "10",
        "country": country,
        "lat": lat,
        "lng": lng,
        "zoom": "13"
    }

    def api_call():
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    return call_api_with_retries(api_call)
