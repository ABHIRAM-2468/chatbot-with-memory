"""
chat_history.py — Persistent Chat History
==========================================
Save and load conversations as JSON files so users
can revisit past chats even after closing the app.
"""

import json
import os
from datetime import datetime
import config


def _ensure_log_dir():
    """Create the chat_logs directory if it doesn't exist."""
    os.makedirs(config.CHAT_LOG_DIR, exist_ok=True)


def save_chat(messages, user_profile=None, filename=None):
    """Save a conversation to a JSON file.

    Args:
        messages: list of message dicts [{"role": ..., "content": ...}]
        user_profile: optional dict of user preferences to save
        filename: optional custom filename (auto-generated if not provided)

    Returns:
        The filename of the saved chat
    """
    _ensure_log_dir()

    if not filename:
        # Generate a timestamp-based filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_{timestamp}.json"

    filepath = os.path.join(config.CHAT_LOG_DIR, filename)

    data = {
        "saved_at": datetime.now().isoformat(),
        "message_count": len(messages),
        "messages": messages,
    }

    if user_profile:
        data["user_profile"] = user_profile

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filename


def load_chat(filename):
    """Load a conversation from a JSON file.

    Args:
        filename: name of the file in chat_logs/

    Returns:
        dict with "messages" and optionally "user_profile",
        or None if the file doesn't exist
    """
    filepath = os.path.join(config.CHAT_LOG_DIR, filename)

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_chats():
    """List all saved conversations, newest first.

    Returns:
        list of dicts with "filename", "saved_at", and "message_count"
    """
    _ensure_log_dir()

    chats = []
    for filename in os.listdir(config.CHAT_LOG_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(config.CHAT_LOG_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            chats.append({
                "filename": filename,
                "saved_at": data.get("saved_at", "Unknown"),
                "message_count": data.get("message_count", 0),
            })
        except (json.JSONDecodeError, IOError):
            continue  # Skip corrupted files

    # Sort newest first
    chats.sort(key=lambda x: x["saved_at"], reverse=True)
    return chats


def delete_chat(filename):
    """Delete a saved conversation.

    Args:
        filename: name of the file to delete

    Returns:
        True if deleted, False if file not found
    """
    filepath = os.path.join(config.CHAT_LOG_DIR, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
