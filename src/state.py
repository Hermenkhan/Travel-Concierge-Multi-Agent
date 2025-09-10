# src/state.py
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class State(BaseModel):
    query: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None
    research_results: Optional[Dict[str, Any]] = None
    city: Optional[str] = None
    weather_summary: Optional[Dict[str, Any]] = None
    recommended_places: Optional[List[Dict[str, Any]]] = None
    outputs: Optional[Dict[str, Any]] = None
    tools_used: List[str] = []
    violations: List[str] = []
    tool_error: bool = False
    failure_count: int = 0
    metadata: Dict[str, Any] = {}
