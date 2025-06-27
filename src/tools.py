from langchain_core.tools import tool
from .utils import get_tavily_extract, get_tavily_search, get_mongo_client, get_logger
from typing import List, Optional

logger = get_logger()
tavily_search = get_tavily_search()
tavily_extract = get_tavily_extract()
mongo_client = get_mongo_client()

@tool(
    description="Query MongoDB for suppliers matching requirements and optional ESG preference."
)
def query_mongodb(requirements: dict, esg_filter: Optional[str] = None) -> List[dict]:
    pass

@tool(
    description=(
        "Use the Tavily API to search online for supplier leads. "
        "Accepts a free-form query string and returns structured JSON results."
    )
)
def web_search(query: str) -> dict:
    """Perform a supplier-lead web search via Tavily."""
    logger.debug(
        "Starting Tavily web search", 
        extra={"query": query}
    )
    response = tavily_search.invoke({"query": query})

    # Log operational summary at INFO level
    logger.info(
        "Completed Tavily web search",
        extra={
            "query": query,
            "result_count": len(response.get("results", [])),
        }
    )
    return response

@tool(
    description=(
        "Use the Tavily API to extract detailed supplier information "
        "from a list of URLs. Returns enriched metadata in JSON form."
    )
)
def web_extract(urls: List[str]) -> dict:
    """Fetch and parse supplier data from provided URLs via Tavily."""
    logger.debug(
        "Starting Tavily extraction",
        extra={"url_count": len(urls), "urls": urls}
    )
    response = tavily_extract.invoke({"urls": urls})

    logger.info(
        "Completed Tavily extraction",
        extra={
            "url_count": len(urls),
        }
    )
    return response
