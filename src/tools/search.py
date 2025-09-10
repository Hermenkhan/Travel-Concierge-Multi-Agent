import os
import requests
import json
from dotenv import load_dotenv
from src.utils.retry import call_api_with_retries

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_api(query: str):
    """Call Serper API with retries"""
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = json.dumps({"q": query})

    def api_call():
        resp = requests.post(url, headers=headers, data=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

    return call_api_with_retries(api_call)
