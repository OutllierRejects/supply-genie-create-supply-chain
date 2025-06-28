from langgraph.graph import StateGraph, START, END
from .agents import requirement_analysis_agent, supply_exploration_agent
from langgraph.graph.state import CompiledStateGraph
from functools import lru_cache
from typing import TypedDict, Dict, Any, Optional
from .models import RequirementAnalysisResponse, SupplierExplorationAgentResponse
import json


class GraphState(TypedDict):
    query: str
    chat_history: Optional[list[Dict[str, Any]]]

    requirement_analysis_response: Optional[RequirementAnalysisResponse]
    supplier_exploration_response: Optional[SupplierExplorationAgentResponse]

    agent_scratchpad: Optional[str]
    messages: Optional[list[Dict[str, Any]]]


def prepare_state(raw_input: dict) -> GraphState:
    """
    Transform the input payload into the expected GraphState format.
    """
    return {
        "query": raw_input.get("query", ""),
        "chat_history": raw_input.get("chat_history"),
        "requirement_analysis_response": None,
        "supplier_exploration_response": None,
        "agent_scratchpad": "",
        "messages": [],
    }


def extract_final_response(
    final_state: Dict[str, Any],
) -> SupplierExplorationAgentResponse:
    """
    Extract the supplier exploration response from the final graph state.
    This handles cases where the response might be nested or in different formats.
    """
    # Check if we have the direct response
    if (
        "supplier_exploration_response" in final_state
        and final_state["supplier_exploration_response"]
    ):
        return final_state["supplier_exploration_response"]

    # Check if it's in messages (common with chat agents)
    if "messages" in final_state and final_state["messages"]:
        last_message = final_state["messages"][-1]
        if hasattr(last_message, "content"):
            content = last_message.content
            # Try to parse JSON from content
            if isinstance(content, str):
                try:
                    parsed_content = json.loads(content)
                    if "suppliers" in parsed_content:
                        return SupplierExplorationAgentResponse(**parsed_content)
                except (json.JSONDecodeError, TypeError):
                    pass
            elif isinstance(content, dict) and "suppliers" in content:
                return SupplierExplorationAgentResponse(**content)

    # Fallback: return empty response
    return SupplierExplorationAgentResponse(suppliers=[])


@lru_cache(maxsize=1)
def get_graph() -> CompiledStateGraph:
    graph = StateGraph(state_schema=GraphState)

    analysis_node = requirement_analysis_agent()
    exploration_node = supply_exploration_agent()

    graph.add_node("requirement_analysis_agent", analysis_node)
    graph.add_node("supply_exploration_agent", exploration_node)

    graph.add_edge(START, "requirement_analysis_agent")
    graph.add_edge("requirement_analysis_agent", "supply_exploration_agent")
    graph.add_edge("supply_exploration_agent", END)

    return graph.compile()
