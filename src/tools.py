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
)

logger = get_logger()
tavily_search = get_tavily_search()
tavily_extract = get_tavily_extract()
mongo_client = get_mongo_client()


@tool(
    description="Query MongoDB for existing suppliers matching the requirements.",
    args_schema=SupplierSearchIndexQuery,
)
def query_mongodb(
    query: str = None,
    location: str = None,
    price_range: str = None,
    specialties: List[str] = None,
    certifications: List[str] = None,
    lead_time: str = None,
) -> List[dict]:
    logger.info("Starting MongoDB query for suppliers")
    logger.info(
        f"Query parameters - query: {query}, location: {location}, price_range: {price_range}"
    )
    logger.debug(
        f"Additional filters - specialties: {specialties}, certifications: {certifications}, lead_time: {lead_time}"
    )

    # Create the query object
    search_query = SupplierSearchIndexQuery(
        query=query,
        location=location,
        price_range=price_range,
        specialties=specialties,
        certifications=certifications,
        lead_time=lead_time,
    )

    logger.debug(f"Query parameters: {search_query.dict()}")

    try:
        create_search_index_if_not_exists()
        logger.debug("Search index verified/created")

        db, collection = get_supplier_db_and_collection()
        query_filter = search_query.build_filter()
        logger.debug(f"Built MongoDB filter: {query_filter}")

        if not query_filter:
            logger.info("No search criteria provided, returning empty results")
            return []

        logger.info("Executing MongoDB find query...")
        results = list(collection.find(query_filter))
        logger.info(f"Found {len(results)} suppliers in MongoDB")

        if results:
            logger.debug(
                f"Sample result keys: {list(results[0].keys()) if results else 'N/A'}"
            )
            for i, result in enumerate(results[:3]):  # Log first 3 results
                company_name = result.get("company_name", "Unknown")
                location = result.get("location", "Unknown")
                logger.debug(f"  {i+1}. {company_name} - {location}")
        else:
            logger.warning("No suppliers found matching the criteria")

        return results

    except Exception as e:
        logger.error(f"MongoDB query failed: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}")
        return []


@tool(
    description=(
        "Use the Tavily API to search online for potential supplier leads. "
        "Accepts a free-form query string describing the desired supplier characteristics "
        "and returns structured JSON results containing search snippets and URLs."
    ),
    args_schema=WebSearchQuery,
)
def web_search(query: str) -> dict:
    logger.info("Starting Tavily web search")
    logger.info(f"Search query: '{query}'")
    logger.debug(f"Query length: {len(query)} characters")

    try:
        logger.debug("Invoking Tavily search API...")
        response = tavily_search.invoke({"query": query})
        logger.debug("Tavily API call completed")

        result_count = (
            len(response.get("results", [])) if isinstance(response, dict) else 0
        )
        logger.info(f"Tavily web search completed - found {result_count} results")

        if isinstance(response, dict) and "results" in response:
            logger.debug(
                f"Response contains {len(response['results'])} results with keys: {list(response.keys())}"
            )
            # Log some sample results for debugging
            for i, result in enumerate(response["results"][:2]):  # First 2 results
                title = result.get("title", "No title")[:50]
                url = result.get("url", "No URL")
                logger.debug(f"  Result {i+1}: {title}... - {url}")

        return response if isinstance(response, dict) else {"results": []}

    except Exception as e:
        logger.error(f"Tavily web search failed: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}")
        return {"results": [], "error": str(e)}


@tool(
    description="Extract detailed supplier information from URLs using Tavily API.",
    args_schema=WebExtractQuery,
)
def web_extract(urls: List[str]) -> dict:
    logger.info(f"Starting Tavily URL extraction for {len(urls)} URLs")
    logger.debug(f"URLs to extract: {urls}")

    if not urls:
        logger.warning("No URLs provided for extraction")
        return {"results": [], "error": "No URLs provided"}

    try:
        logger.debug("Invoking Tavily extract API...")
        response = tavily_extract.invoke({"urls": urls})
        logger.info("Tavily extraction completed successfully")

        if isinstance(response, dict):
            logger.debug(f"Response keys: {list(response.keys())}")
            if "results" in response:
                logger.debug(f"Extracted {len(response['results'])} page contents")

        return response

    except Exception as e:
        logger.error(f"Tavily extraction failed: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}")
        return {"results": [], "error": str(e)}


@tool(description="Complete the supplier search and return the final results.")
def finalize_supplier_search(suppliers: List[Supplier]) -> dict:
    logger.info(f"Finalizing supplier search with {len(suppliers)} suppliers")

    if not suppliers:
        logger.warning("No suppliers provided for finalization")
    else:
        logger.debug("Supplier summary:")
        for i, supplier in enumerate(suppliers[:5]):  # Log first 5
            name = (
                supplier.company_name
                if hasattr(supplier, "company_name")
                else str(supplier)[:50]
            )
            logger.debug(f"  {i+1}. {name}")
        if len(suppliers) > 5:
            logger.debug(f"  ... and {len(suppliers) - 5} more suppliers")

    result = {
        "suppliers": [supplier.dict() for supplier in suppliers],
        "count": len(suppliers),
    }

    logger.info(f"Search completed successfully with {len(suppliers)} suppliers")
    logger.debug(
        f"Result structure: count={result['count']}, suppliers_type={type(result['suppliers'])}"
    )
    return result
