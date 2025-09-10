# src/agents/reviewer.py
from src.state import State
from src.guardrails.schemas import ItineraryOutput

def reviewer_node(state: State) -> State:
    if not isinstance(state, State):
        state = State.parse_obj(state)

    # If outputs exist but failed schema, attempt to repair (simple heuristic)
    outputs = state.outputs or {}
    try:
        # try to coerce and validate
        validated = ItineraryOutput.parse_obj(outputs)
        state.outputs = validated.dict()
        return state
    except Exception as e:
        state.violations.append("Reviewer failed to repair: " + str(e))
        # Mark partial and return
        state.outputs = {
            "city": outputs.get("city", state.city),
            "days": outputs.get("days", 1),
            "plan": outputs.get("plan", []) or [{"day":1,"activities":[{"time":"any","place":"TBD","type":"unknown"}]}],
            "weather_forecast": outputs.get("weather_forecast", "unknown"),
            "sources": outputs.get("sources", [])
        }
        return state
