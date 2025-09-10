# src/agents/executor.py
import os
import json
import time
from langchain_groq import ChatGroq  # keep provider
from src.state import State
from src.guardrails.schemas import ItineraryOutput
from src.guardrails.moderation import prompt_hardening, basic_moderation_check
from src.fallbacks import cached_places_stub

GROQ_KEY = os.getenv("GROQ_API_KEY", "priavte")
llm = ChatGroq(model="moonshotai/kimi-k2-instruct", api_key=GROQ_KEY)

SYSTEM_PROMPT = """
You are a travel assistant. Produce only JSON that conforms exactly to the supplied schema.
Do NOT ask for secrets. Do NOT include any PII beyond city names. If unable to produce full output, return partial but valid JSON that still validates.
"""

def executor_node(state: State) -> State:
    if not isinstance(state, State):
        state = State.parse_obj(state)

    city = state.city or state.plan.get("city", "Unknown City")
    weather = state.weather_summary or {}
    places = state.recommended_places or []

    schema_json = ItineraryOutput.schema_json(indent=2)
    user_prompt = f"""
Create a {state.plan.get('days', 3)}-day itinerary for {city}.
Weather summary: {json.dumps(weather)}
Places (optional): {json.dumps(places)}

Return output strictly in this JSON format:
{schema_json}
    """

    system_prompt = prompt_hardening(SYSTEM_PROMPT)
    max_retries = 2
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            # Use the hardened system prompt; depending on ChatGroq usage adapt call:
            resp = llm.invoke([{"role": "system", "content": system_prompt},
                               {"role": "user", "content": user_prompt}], timeout=20)
            # The exact shape of resp depends on the provider; adapt if needed:
            content = resp.content if hasattr(resp, "content") else resp[0].content
            # moderation check
            mod = basic_moderation_check(content)
            if not mod["ok"]:
                state.violations.append("Executor failed moderation: " + mod["reason"])
                # route to reviewer: set a flag and return partial
                state.metadata["route_to_reviewer"] = True
                return state

            plan_json = json.loads(content)
            valid = ItineraryOutput.parse_obj(plan_json)
            state.outputs = valid.dict()
            return state

        except Exception as e:
            last_exception = e
            state.failure_count += 1
            state.violations.append(f"Executor attempt {attempt+1} failed: {str(e)}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                break

    # Last-resort fallback
    fallback_plan = {
        "city": city,
        "days": 1,
        "plan": [
            {
                "day": 1,
                "activities": [
                    {"time": "morning", "place": "Central Park", "type": "sightseeing"},
                    {"time": "evening", "place": places[0]["name"] if places and isinstance(places[0], dict) else "Local Restaurant", "type": "restaurant"}
                ]
            }
        ],
        "weather_forecast": "Data unavailable, please check manually.",
        "sources": []
    }

    state.outputs = fallback_plan
    state.violations.append("Executor fell back to minimal itinerary.")
    state.tool_error = True
    return state

    
