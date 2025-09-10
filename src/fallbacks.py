# src/fallbacks.py
import time
import json
from typing import Callable

CIRCUIT_BREAKER_THRESHOLD = 4

def cached_weather_stub(city: str):
    return {"summary": "Weather data unavailable (cached stub).", "fallback": True}

def cached_places_stub(city: str, interest: str):
    return {"places": [{"name": f"Popular {interest.title()} — {city}", "rating": 4.0}], "fallback": True}

def should_trip_fail_shortcircuit(state) -> bool:
    return getattr(state, "failure_count", 0) >= CIRCUIT_BREAKER_THRESHOLD

def retry_with_backoff(func: Callable, max_retries=2, base_delay=1.0):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries:
                sleep = base_delay * (2 ** attempt)
                time.sleep(sleep)
            else:
                raise
