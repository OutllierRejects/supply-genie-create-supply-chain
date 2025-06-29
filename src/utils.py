from functools import lru_cache
from pymongo import MongoClient
from pymongo.collection import Collection
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from .config import (
    OPENAI_API_KEY,
    GOOGLE_API_KEY,
    MONGO_URI,
    MODEL_NAME,
    LLM_TEMPERATURE,
    TAVILY_API_KEY,
    MAX_TOKENS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
)

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilyExtract
from langchain_tavily import TavilySearch
from loguru import logger
from .config import SEARCH_INDEX_NAME, SEARCH_INDEX_SPEC
from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache
def get_logger() -> logger:
    return logger


@lru_cache
def get_mongo_client() -> MongoClient:
    return MongoClient(MONGO_URI)


# @lru_cache
# def get_llm() -> ChatOpenAI:
#     return ChatOpenAI(
#         temperature=LLM_TEMPERATURE,
#         model=MODEL_NAME,
#         api_key=OPENAI_API_KEY,
#         max_tokens=MAX_TOKENS,
#         timeout=REQUEST_TIMEOUT,
#         max_retries=MAX_RETRIES,
#     )
@lru_cache
def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        temperature=LLM_TEMPERATURE,
        model=MODEL_NAME,
        api_key=GOOGLE_API_KEY,
        max_tokens=MAX_TOKENS,
        timeout=REQUEST_TIMEOUT,
        max_retries=MAX_RETRIES,
    )


@lru_cache
def get_tavily_search() -> TavilySearch:
    return TavilySearch(api_key=TAVILY_API_KEY)


@lru_cache
def get_tavily_extract() -> TavilyExtract:
    return TavilyExtract(api_key=TAVILY_API_KEY)


@lru_cache
def get_supplier_db_and_collection() -> tuple[MongoClient, Collection]:
    """
    Returns the MongoDB database and collection for suppliers.
    """
    client = get_mongo_client()
    db = client["supplier_db"]
    collection = db["suppliers"]
    return db, collection

@lru_cache
def get_async_supplier_db_and_collection():
    """
    Returns async MongoDB database and collection for suppliers.
    """
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["supplier_db"]
    collection = db["suppliers"]
    return db, collection


def create_search_index_if_not_exists() -> None:
    """
    Create a text index on the collection if it does not already exist.
    Fixed: Get collection within function to match usage in tools.py
    """
    db, collection = get_supplier_db_and_collection()
    if SEARCH_INDEX_NAME not in collection.index_information():
        collection.create_index(
            SEARCH_INDEX_SPEC, name=SEARCH_INDEX_NAME, default_language="english"
        )


def save_suppliers_to_mongodb(suppliers: list) -> dict:
    """
    Save suppliers to MongoDB for future retrieval and analysis.

    Args:
        suppliers: List of supplier dictionaries or objects

    Returns:
        dict: Result of the save operation
    """
    try:
        logger.info(f"Saving {len(suppliers)} suppliers to MongoDB")

        # Get database and collection
        db, collection = get_supplier_db_and_collection()

        # Ensure search index exists
        create_search_index_if_not_exists()

        # Convert suppliers to dictionaries if they're Pydantic models
        supplier_dicts = []
        for supplier in suppliers:
            if hasattr(supplier, "dict"):
                # Pydantic model
                supplier_dict = supplier.dict()
            elif hasattr(supplier, "__dict__"):
                # Regular object
                supplier_dict = supplier.__dict__
            else:
                # Already a dict
                supplier_dict = supplier

            supplier_dicts.append(supplier_dict)

        if supplier_dicts:
            # Insert suppliers into MongoDB
            result = collection.insert_many(supplier_dicts)
            logger.info(
                f"Successfully saved {len(result.inserted_ids)} suppliers to MongoDB"
            )
            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "inserted_ids": [str(id) for id in result.inserted_ids],
            }
        else:
            logger.warning("No suppliers to save")
            return {
                "success": True,
                "inserted_count": 0,
                "message": "No suppliers to save",
            }

    except Exception as e:
        logger.error(f"Error saving suppliers to MongoDB: {str(e)}", exc_info=True)
        return {"success": False, "error": str(e), "inserted_count": 0}


async def save_suppliers_to_mongodb_async(suppliers: list) -> dict:
    """
    Async version of save_suppliers_to_mongodb for better performance.
    
    Args:
        suppliers: List of supplier dictionaries or objects
        
    Returns:
        dict: Result of the save operation
    """
    try:
        logger.info(f"Async saving {len(suppliers)} suppliers to MongoDB")
        
        # Get async database and collection
        db, collection = get_async_supplier_db_and_collection()
        
        # Convert suppliers to dictionaries if they're Pydantic models
        supplier_dicts = []
        for supplier in suppliers:
            if hasattr(supplier, 'model_dump'):
                supplier_dict = supplier.model_dump()
            elif hasattr(supplier, 'dict'):
                supplier_dict = supplier.dict()
            else:
                supplier_dict = dict(supplier) if isinstance(supplier, dict) else supplier
            
            # Add metadata
            supplier_dict["_created_at"] = datetime.utcnow()
            supplier_dict["_source"] = "supply_chain_agent"
            supplier_dicts.append(supplier_dict)
        
        if supplier_dicts:
            # Insert documents asynchronously
            result = await collection.insert_many(supplier_dicts)
            logger.success(
                f"Successfully saved {len(result.inserted_ids)} suppliers to MongoDB (async)"
            )
            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "inserted_ids": [str(id) for id in result.inserted_ids],
            }
        else:
            logger.warning("No suppliers to save")
            return {
                "success": True,
                "inserted_count": 0,
                "message": "No suppliers to save",
            }

    except Exception as e:
        logger.error(f"Error saving suppliers to MongoDB (async): {str(e)}", exc_info=True)
        return {"success": False, "error": str(e), "inserted_count": 0}


# TODO: Timer Logger Decorator
