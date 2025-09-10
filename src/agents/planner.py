import re
from src.state import State

def extract_days(query: str) -> int:
    """Extract number of days from query, default = 3."""
    match = re.search(r"(\d+)\s*day", query.lower())
    return int(match.group(1)) if match else 3

def extract_city(query: str) -> str:
    """Naive city extraction (you can enhance later with NER)."""
    # Look for "to <city>"
    match = re.search(r"to\s+([A-Z][a-zA-Z ]+)", query)
    return match.group(1).strip() if match else "New York"

def extract_interests(query: str) -> list:
    """Extract interest keywords like museum, restaurant, park, etc."""
    interests = []
    keywords = ["museum", "restaurant", "park", "shopping", "beach", "landmark", "hiking"]
    for kw in keywords:
        if kw in query.lower():
            interests.append(kw)
    return interests or ["general sightseeing"]

def planner_node(state: State) -> State:
    """Planner agent: parse user query into structured plan."""
    query = state["query"]

    days = extract_days(query)
    city = extract_city(query)
    interests = extract_interests(query)

    plan = {
        "city": city,
        "days": days,
        "interests": interests
    }

    # Update state
    new_state = {**state, "plan": plan}
    return new_state
