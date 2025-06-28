from langchain_core.tools import tool
from .utils import (
    get_tavily_extract,
    get_tavily_search,
    get_mongo_client,
    get_logger,
    create_search_index_if_not_exists,
    get_supplier_db_and_collection,
)
from typing import List
from .models import (
    SupplierSearchIndexQuery,
    WebSearchQuery,
    WebExtractQuery,
    Supplier,
    SupplierExplorationAgentResponse,
)

logger = get_logger()
tavily_search = get_tavily_search()
tavily_extract = get_tavily_extract()
mongo_client = get_mongo_client()


@tool(
    description=(
        "Query MongoDB for suppliers matching specific requirements, "
        "including product types, certifications, and optional ESG preferences. "
        "Returns a list of supplier dictionaries."
    ),
    args_schema=SupplierSearchIndexQuery,
)
def query_mongodb(supplier_search_index_query: SupplierSearchIndexQuery) -> List[dict]:
    logger.debug(
        "Starting MongoDB query",
        extra={"query": supplier_search_index_query.dict()},
    )
    create_search_index_if_not_exists()
    db, collection = get_supplier_db_and_collection()
    query_filter = supplier_search_index_query.build_filter()
    results = list(collection.find(query_filter))
    logger.info(
        "Completed MongoDB query", extra={"result_count": len(results)}
    )  # Added logging
    return results


@tool(
    description=(
        "Use the Tavily API to search online for potential supplier leads. "
        "Accepts a free-form query string describing the desired supplier characteristics "
        "and returns structured JSON results containing search snippets and URLs."
    ),
    args_schema=WebSearchQuery,
)
def web_search(query: str) -> dict:
    logger.debug("Starting Tavily web search", extra={"query": query})
    response = tavily_search.invoke({"query": query})

    logger.info(
        "Completed Tavily web search",
        extra={
            "query": query,
            "result_count": len(response.get("results", [])),
        },
    )
    return response


@tool(
    description=(
        "Use the Tavily API to extract detailed supplier information from a list of URLs. "
        "This tool retrieves and parses content from the given URLs, "
        "extracting key metadata such as company descriptions, contact information, "
        "certifications, and ESG ratings. Returns enriched metadata in JSON format."
    ),
    args_schema=WebExtractQuery,
)
def web_extract(urls: List[str]) -> dict:
    logger.debug(
        "Starting Tavily extraction", extra={"url_count": len(urls), "urls": urls}
    )
    response = tavily_extract.invoke({"urls": urls})

    logger.info(
        "Completed Tavily extraction",
        extra={
            "url_count": len(urls),
        },
    )
    return response


@tool(description="Finalize supplier search and return results")
def finalize_supplier_search(
    suppliers: List[Supplier],
) -> SupplierExplorationAgentResponse:
    return SupplierExplorationAgentResponse(suppliers=suppliers)
