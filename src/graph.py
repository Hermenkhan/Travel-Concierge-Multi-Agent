# src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import State
from src.agents.researcher import researcher_node
from src.agents.planner import planner_node
from src.agents.executor import executor_node
from src.observability import record_run_trace
from src.fallbacks import should_trip_fail_shortcircuit

def build_graph():
    graph = StateGraph(State)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("executor", executor_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    # conditional edges: if researcher indicates tool_error route straight to executor but set reduced_scope
    def researcher_to_executor_condition(state):
        # short-circuit if too many failures
        if should_trip_fail_shortcircuit(state):
            state.outputs = {"summary": "Service degraded. Partial results only."}
            return "END"  # or route to END node
        return True

    graph.add_edge("researcher", "executor", condition=researcher_to_executor_condition)
    graph.add_edge("executor", END)
    return graph.compile()

graph = build_graph()

if __name__ == "__main__":
    inputs = {"query": "3 day trip to New York focused on museum and parks"}
    run = graph.invoke(inputs)
    # record trace (you should build a trace object inside your graph run - simplified example)
    trace = {
        "run_inputs": inputs,
        "outputs": run.get("outputs"),
        "failures": run.get("violations", []),
        "tools_used": run.get("tools_used", [])
    }
    run_id = "localrun1"
    trace_path = record_run_trace(run_id, trace)
    print("result:", run.get("outputs"))
    print("trace saved:", trace_path)
