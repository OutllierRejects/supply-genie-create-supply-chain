# src/config.py - Complete with all required constants
from pymongo import TEXT
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys and Database
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
LLM_TEMPERATURE = 0.0

# MongoDB Configuration
SEARCH_INDEX_NAME = "supplier_search_index"
SEARCH_INDEX_SPEC = [("$**", TEXT)]

# Agent Configuration - ADD THESE MISSING CONSTANTS
MAX_QUERY_LENGTH = 1000
MAX_EXTRACT_URLS = 10
DEFAULT_REMAINING_STEPS = 10
AGENT_MAX_SUPPLIERS = 10
AGENT_RECURSION_LIMIT = 15
