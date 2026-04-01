"""
llm.py — Multi-Provider LLM Integration
=========================================
Supports Groq, Google Gemini, and OpenAI.
Switch provider by setting LLM_PROVIDER in .env

Default: Groq (free, fastest)
"""

import config

# ------------------------------------------------------------------ #
#  System Prompts
# ------------------------------------------------------------------ #

NORMAL_PROMPT = """You are a helpful, friendly AI assistant called "Anti-Gravity AI".
You give clear, concise, and accurate answers.
You remember context from the conversation and personalize your responses.
Be warm and engaging — make the user feel like they're talking to a next-gen AI."""

ANTIGRAVITY_PROMPT = """You are "Anti-Gravity AI" — an assistant that defies conventional thinking.

For EVERY response, you MUST use this exact dual-thinking format:

🧱 **Ground Floor** (Practical Answer)
[Give a solid, well-structured, practical answer to the user's question]

🚀 **Gravity Break** (Creative Twist)
[Now reframe the problem in an unexpected way. Think like a mix of engineer, scientist, and creator. Provide a bold, innovative, slightly futuristic alternative idea or perspective]

Rules:
- Always include BOTH sections in every response
- Ground Floor should be genuinely useful and actionable
- Gravity Break should surprise the user — make them think "I never thought of it that way"
- Keep both sections engaging and well-written
- Adapt your style based on the user's preferences and context
- Be warm, slightly futuristic, and make the user feel special"""


def get_system_prompt(mode, profile_context=""):
    """Build the full system prompt based on mode + user profile."""
    base = ANTIGRAVITY_PROMPT if mode == "Anti-Gravity" else NORMAL_PROMPT
    if profile_context:
        base += profile_context
    return base


# ------------------------------------------------------------------ #
#  Provider Implementations
# ------------------------------------------------------------------ #

def _call_groq(messages, mode, profile_context):
    """Call Groq API (OpenAI-compatible, free tier)."""
    from groq import Groq
    client = Groq(api_key=config.GROQ_API_KEY)

    system_prompt = get_system_prompt(mode, profile_context)
    api_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=api_messages,
        max_tokens=config.MAX_TOKENS,
        temperature=config.TEMPERATURE,
    )
    return response.choices[0].message.content


def _call_gemini(messages, mode, profile_context):
    """Call Google Gemini API (free tier)."""
    import google.generativeai as genai
    genai.configure(api_key=config.GEMINI_API_KEY)

    model = genai.GenerativeModel(
        model_name=config.MODEL_NAME,
        system_instruction=get_system_prompt(mode, profile_context),
    )

    # Convert messages to Gemini format
    # Gemini uses "user"/"model" roles (not "assistant")
    history = []
    last_user_msg = ""

    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        if msg == messages[-1] and role == "user":
            last_user_msg = msg["content"]
        else:
            history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=history)
    response = chat.send_message(last_user_msg or messages[-1]["content"])
    return response.text


def _call_openai(messages, mode, profile_context):
    """Call OpenAI API (requires paid key)."""
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    system_prompt = get_system_prompt(mode, profile_context)
    api_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=api_messages,
        max_tokens=config.MAX_TOKENS,
        temperature=config.TEMPERATURE,
    )
    return response.choices[0].message.content


# ------------------------------------------------------------------ #
#  Main Entry Point
# ------------------------------------------------------------------ #

def get_response(messages, mode="Normal", profile_context=""):
    """Route to the correct LLM provider and return the AI's response.

    Args:
        messages: list of {role, content} dicts (conversation history)
        mode: "Normal" or "Anti-Gravity"
        profile_context: formatted user profile for personalization

    Returns:
        AI response string
    """
    provider = config.LLM_PROVIDER.lower()

    try:
        if provider == "groq":
            return _call_groq(messages, mode, profile_context)
        elif provider == "gemini":
            return _call_gemini(messages, mode, profile_context)
        elif provider == "openai":
            return _call_openai(messages, mode, profile_context)
        else:
            return f"❌ Unknown provider `{provider}`. Set `LLM_PROVIDER` to `groq`, `gemini`, or `openai` in `.env`."

    except Exception as e:
        error = str(e).lower()

        if "api_key" in error or "authentication" in error or "401" in error or "invalid_api_key" in error:
            key_var = {
                "groq": "GROQ_API_KEY",
                "gemini": "GEMINI_API_KEY",
                "openai": "OPENAI_API_KEY",
            }.get(provider, "API_KEY")

            get_key_url = {
                "groq": "https://console.groq.com/keys",
                "gemini": "https://aistudio.google.com/app/apikey",
                "openai": "https://platform.openai.com/api-keys",
            }.get(provider, "#")

            return (
                f"⚠️ **API Key Error ({provider.upper()})**\n\n"
                f"Your `{key_var}` is missing or invalid.\n\n"
                f"**How to fix:**\n"
                f"1. Get a free key from [{get_key_url}]({get_key_url})\n"
                f"2. Open your `.env` file\n"
                f"3. Set: `{key_var}=your-key-here`\n"
                f"4. Restart the app"
            )

        if "rate_limit" in error:
            return "⏳ **Rate limited.** Please wait a moment and try again."

        return f"❌ **Error:** {str(e)}"
