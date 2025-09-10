# src/agents/researcher.py
import json
import time
from src.state import State
from src.tools.search import search_api
from src.tools.weather import weather_api
from src.tools.places import places_api
from src.fallbacks import cached_weather_stub, cached_places_stub
from src.guardrails.schemas import ItineraryOutput

def researcher_node(state: State) -> State:
    """Researcher agent: fetch weather + places info based on the plan."""
    # Accept either State instance or dict
    if not isinstance(state, State):
        state = State.parse_obj(state)

    plan = state.plan or {}
    city = plan.get("city", "New York")
    interests = plan.get("interests", ["museum", "restaurant"])

    # initialize
    research = {"city": city, "weather_summary": None, "recommended_places": [], "sources": []}
    try:
        # weather call (uses call_api_with_retries internally)
        weather_resp = weather_api(city)
        if weather_resp.get("fallback"):
            state.tool_error = True
            research["weather_summary"] = cached_weather_stub(city)
            state.tools_used.append("weather_api_fallback")
        else:
            research["weather_summary"] = weather_resp
            state.tools_used.append("weather_api")
            research["sources"].append("openweather/rapidapi")

        # places for each interest
        for interest in interests:
            places_resp = places_api(query=interest, lat=plan.get("lat","40.7128"), lng=plan.get("lng","-74.0060"))
            if places_resp.get("fallback"):
                state.tool_error = True
                places_data = cached_places_stub(city, interest)
                state.tools_used.append("places_api_fallback")
            else:
                places_data = places_resp
                state.tools_used.append("places_api")
            research["recommended_places"].append({"interest": interest, "data": places_data})

        # search context (optional)
        search_resp = search_api(f"Top attractions in {city}")
        if search_resp.get("fallback"):
            state.tools_used.append("search_api_fallback")
        else:
            state.tools_used.append("search_api")
            research["sources"].append("serper")

    except Exception as e:
        state.failure_count += 1
        state.violations.append(f"Researcher error: {str(e)}")
        # Attach a lightweight fallback: minimal info
        state.tool_error = True
        research["error"] = str(e)

    state.research_results = research
    # also propagate convenient fields
    state.city = city
    state.weather_summary = research.get("weather_summary")
    state.recommended_places = [p["data"] for p in research["recommended_places"]]

    return state
