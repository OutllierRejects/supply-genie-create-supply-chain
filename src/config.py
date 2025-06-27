from functools import lru_cache 
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
LLM_TEMPERATURE = 0.0

