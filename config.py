"""
config.py — Configuration & Environment Loader
================================================
Supports multiple LLM providers:
  - Groq  (default, free & fastest)
  - Gemini (Google, free tier)
  - OpenAI (if you have a key)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---- Provider Selection ----
# Options: "groq" | "gemini" | "openai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

# ---- API Keys ----
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")

# ---- Model Names per Provider ----
MODELS = {
    "groq":   "llama-3.3-70b-versatile",   # Fast, free, powerful (updated)
    "gemini": "gemini-1.5-flash",           # Google, free tier
    "openai": "gpt-3.5-turbo",
}

MODEL_NAME   = MODELS.get(LLM_PROVIDER, MODELS["groq"])
MAX_TOKENS   = 1024
TEMPERATURE  = 0.7

# ---- Memory Settings ----
CONTEXT_WINDOW = 20
CHAT_LOG_DIR   = "chat_logs"

# ---- App Settings ----
APP_TITLE    = "🧠 Chatbot with Memory"
APP_ICON     = "🚀"
DEFAULT_MODE = "Normal"
