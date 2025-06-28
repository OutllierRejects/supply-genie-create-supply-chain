from functools import lru_cache
from pymongo import MongoClient
from pymongo.collection import Collection
from .config import (
    OPENAI_API_KEY,
    MONGO_URI,
    MODEL_NAME,
    LLM_TEMPERATURE,
    TAVILY_API_KEY,
)

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilyExtract
from langchain_tavily import TavilySearch
from loguru import logger
from .config import SEARCH_INDEX_NAME, SEARCH_INDEX_SPEC


@lru_cache
def get_logger() -> logger:
    return logger


@lru_cache
def get_mongo_client() -> MongoClient:
    return MongoClient(MONGO_URI)


@lru_cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        temperature=LLM_TEMPERATURE,
        model=MODEL_NAME,
        api_key=OPENAI_API_KEY,
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


# TODO: Timer Logger Decorator
