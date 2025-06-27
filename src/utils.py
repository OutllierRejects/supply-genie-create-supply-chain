from functools import lru_cache from .config import OPENAI_API_KEY, MONGO_URI, MODEL_NAME, LLM_TEMPERATURE, TAVILY_API_KEY

@lru_cache
def get_logger():
    from loguru import logger
    return logger

@lru_cache
def get_mongo_client() -> "MongoClient":
    from pymongo import MongoClient
    return MongoClient(MONGO_URI)

@lru_cache
def get_llm() -> "ChatOpenAI":
    from langchain.chat_models import ChatOpenAI
    return ChatOpenAI(temperature=LLM_TEMPERATURE, model_name=MODEL_NAME, OPENAI_API_KEY=OPENAI_API_KEY)

@lru_cache
def get_tavily_search() -> "TavilySearch":
    from langchain_tavily import TavilySearch
    return TavilySearch(api_key=TAVILY_API_KEY)

@lru_cache
def get_tavily_extract() -> "TavilyExtract":
    from langchain_tavily import TavilyExtract
    return TavilyExtract(api_key=TAVILY_API_KEY)

# TODO: Timer Logger Decorator
