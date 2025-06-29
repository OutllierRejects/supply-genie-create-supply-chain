# src/config.py - Complete with all required constants
from pymongo import TEXT
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys and Database
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-pro")
LLM_TEMPERATURE = 0.2  # Slightly higher for Gemini's creative reasoning

# MongoDB Configuration
SEARCH_INDEX_NAME = "supplier_search_index"
SEARCH_INDEX_SPEC = [("$**", TEXT)]

# Agent Configuration - ADD THESE MISSING CONSTANTS
MAX_QUERY_LENGTH = 2000
MAX_EXTRACT_URLS = 15
DEFAULT_REMAINING_STEPS = 25
AGENT_MAX_SUPPLIERS = 10
AGENT_RECURSION_LIMIT = 200

# LLM Performance Configuration - Optimized for Gemini 2.5 Pro
MAX_TOKENS = 8192  # Increased for Gemini 2.5 Pro's better context handling  
REQUEST_TIMEOUT = 300
MAX_RETRIES = 3 
