from langgraph.prebuilt import create_react_agent
from .utils import get_logger, get_llm
from .models import (
    RequirementAnalysisResponse,
    AgentConfig,
    SupplierExplorationAgentResponse,
)
from langgraph.graph.state import CompiledStateGraph
from .prompts import (
    get_requirement_analysis_agent_prompt,
    get_supply_exploration_agent_prompt,
)
from .tools import web_extract, web_search, query_mongodb, finalize_supplier_search

llm = get_llm()
logger = get_logger()


def requirement_analysis_agent() -> CompiledStateGraph:
    return create_react_agent(
        model=llm,
        prompt=get_requirement_analysis_agent_prompt,
        tools=[],
        response_format=RequirementAnalysisResponse,
        config_schema=AgentConfig,
        name="requirement_analysis_agent",
    )


def supply_exploration_agent() -> CompiledStateGraph:
    tools = [web_extract, web_search, query_mongodb, finalize_supplier_search]
    return create_react_agent(
        llm,
        prompt=get_supply_exploration_agent_prompt,
        tools=tools,
        response_format=SupplierExplorationAgentResponse,
        name="supply_exploration_agent",
    )
