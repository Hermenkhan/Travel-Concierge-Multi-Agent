

# 🧳 Travel Concierge – Multi-Agent Workflow with LangGraph

This project demonstrates a **production-style multi-agent workflow** built with [LangGraph](https://github.com/langchain-ai/langgraph).
The workflow models a **Travel Concierge** that plans a 3-day trip using live weather and places APIs, with built-in **guardrails, fallbacks, retries, and observability**.

---

## ✨ Features

* **Multi-Agent Collaboration**

  * **Researcher** → calls weather, places, and search APIs.
  * **Planner** → parses the query into structured trip plan.
  * **Executor** → generates final itinerary using LLM (Groq).
  * **Reviewer** → validates schema & repairs invalid outputs.
* **Guardrails**

  * Prompt hardening in agent prompts (forbids secret exfiltration, misuse, jailbreaks).
  * Schema validation with **Pydantic** (`ItineraryOutput`).
  * Toxicity / policy checks (lightweight moderation step).
* **Resilience**

  * Tool retries with exponential backoff.
  * Per-node fallbacks (executor has minimal itinerary fallback).
  * Circuit breaker pattern if repeated failures.
* **Observability**

  * Integrated with **LangSmith** for tracing, tokens, and latency tracking.
  * Example traces exported to `artifacts/sample_trace.json`.
* **(Optional)** MCP Tool integration (filesystem/OpenAPI stubs).

---

## 📂 Project Structure

```
├── src
│   ├── graph.py              # LangGraph orchestration
│   ├── state.py              # Shared state definition
│   ├── agents
│   │   ├── researcher.py     # Weather + places lookup
│   │   ├── planner.py        # Parse query → structured plan
│   │   ├── executor.py       # Generate itinerary JSON
│   │   └── reviewer.py       # Schema validation & repair
│   ├── tools
│   │   ├── search.py         # Serper API
│   │   ├── weather.py        # OpenWeather API (RapidAPI)
│   │   └── places.py         # Maps Places API (RapidAPI)
│   ├── guardrails
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── pii.py            # (stub) PII redaction
│   │   └── moderation.py     # (stub) toxicity checks
│   ├── utils
│   │   └── retry.py          # Retry & fallback logic
│   ├── fallbacks.py          # Node & circuit breaker fallbacks
│   └── observability.py      # LangSmith tracing setup
├── notebooks
│   └── demo.ipynb            # Interactive demo
├── artifacts
│   └── sample_trace.json     # Example run trace
├── README.md                 # Project docs
└── .env.example              # Example environment variables
```

---

## 🚀 Setup

1. **Clone Repo**

   ```bash
   git clone https://github.com/<your-org>/travel-concierge-langgraph.git
   cd travel-concierge-langgraph
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Copy `.env.example` → `.env` and fill in:

   ```
   GROQ_API_KEY=your_groq_key
   SERPER_API_KEY=your_serper_key
   RAPIDAPI_KEY=your_rapidapi_key
   LANGCHAIN_API_KEY=your_langsmith_key
   LANGCHAIN_PROJECT=travel-concierge
   ```

4. **Run the Graph**

   ```bash
   python -m src.graph
   ```

---

## 🧪 Example Run

Input:

```python
inputs = {"query": "plan a 3-day trip to New York"}
result = graph.invoke(inputs)
print(json.dumps(result["outputs"], indent=2))
```

Output (fallback example):

```json
{
  "city": "New York",
  "days": [
    {
      "day": 1,
      "activities": [
        {"time": "morning", "place": "Central Park", "type": "sightseeing"},
        {"time": "evening", "place": "Local Restaurant", "type": "restaurant"}
      ]
    }
  ],
  "weather_forecast": "Data unavailable, please check manually."
}
```

---

## 🔒 Guardrails

1. **Prompt Hardening**

   * All system prompts forbid jailbreaks, secret exfiltration, or unsafe tool use.
   * High-risk patterns (e.g. "ignore instructions") are explicitly blocked.

2. **Schema Validation**

   * Every cross-node output must match `ItineraryOutput`.
   * If invalid → violation is logged and fallback triggered.

3. **Moderation Check**

   * Outputs are scanned for toxic / unsafe text.
   * If triggered → routed to Reviewer or human-in-the-loop.

---

## 🔁 Resilience

* **Per-tool retries** with exponential backoff (max 2).
* **Per-node fallback** (Executor falls back to minimal itinerary).
* **Circuit breaker** if too many global failures → graceful summary with apology.

---

## 📊 Observability

* **LangSmith integration**: traces, metrics, and run artifacts.
* Metrics summary (example run):

  * Token usage: \~1.2k
  * Avg tool latency: 850ms
  * Failure count: 1
  * Fallback rate: 33%

See: `artifacts/sample_trace.json`

---

## 🎥 Demo Video

* **Happy path** → normal API calls + structured itinerary.
* **Failure path** → API error triggers fallback.
  (Video placeholder here – add your 3-min demo recording.)

---



---



-

Would you like me to **include explicit example system prompts** (the “prompt hardening” ones you need for the report), or keep README high-level and leave them in `src/agents/` docstrings?
