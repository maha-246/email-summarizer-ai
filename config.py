import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API Keys (Loaded from environment, NOT hardcoded)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model Selections
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite-preview")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# App Constraints
MAX_CHARS = 6000
MIN_CHARS = 20

# Testing / Debugging
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

