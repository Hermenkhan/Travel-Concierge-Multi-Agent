import os
import requests
from dotenv import load_dotenv
from src.utils.retry import call_api_with_retries

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def weather_api(city: str, lang="EN"):
    """Call OpenWeather API with retries"""
    url = "https://open-weather13.p.rapidapi.com/city"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "open-weather13.p.rapidapi.com"
    }
    params = {"city": city, "lang": lang}

    def api_call():
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    return call_api_with_retries(api_call)
