# src/guardrails/schemas.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Activity(BaseModel):
    time: str
    place: str
    type: str
    notes: Optional[str] = None

class DayPlan(BaseModel):
    day: int = Field(..., ge=1)
    activities: List[Activity]

class ItineraryOutput(BaseModel):
    city: str
    days: int = Field(..., ge=1)
    plan: List[DayPlan]
    weather_forecast: Optional[str] = None
    sources: Optional[List[str]] = []

    @validator("plan")
    def days_and_plan_length_match(cls, v, values):
        days = values.get("days")
        if days is None:
            return v
        if len(v) != days:
            raise ValueError("length of plan must equal `days`")
        return v
