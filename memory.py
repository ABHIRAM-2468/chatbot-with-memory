"""
memory.py — Adaptive Memory Manager
=====================================
Handles two types of memory:
1. Conversation history  — the list of messages in the current chat
2. User profile          — persistent preferences (name, interests, goals)

The user profile is automatically extracted from conversation
and injected into the AI's context for personalized responses.
"""


class MemoryManager:
    """Manages conversation history and user preferences."""

    def __init__(self):
        # Full list of messages: [{"role": "user"/"assistant", "content": "..."}]
        self.messages = []

        # User profile — automatically learned from conversation
        self.user_profile = {
            "name": None,
            "interests": [],
            "goals": [],
            "preferences": [],
        }

    # ------------------------------------------------------------------ #
    #  Conversation History
    # ------------------------------------------------------------------ #

    def add_message(self, role, content):
        """Add a message to conversation history.

        Args:
            role: "user" or "assistant"
            content: the message text
        """
        self.messages.append({"role": role, "content": content})

        # Auto-learn preferences from user messages
        if role == "user":
            self._extract_preferences(content)

    def get_history(self):
        """Return the full conversation history."""
        return list(self.messages)

    def get_context_window(self, window_size=20):
        """Return the last N messages for the AI context.

        Args:
            window_size: number of recent messages to include
        Returns:
            list of the most recent messages
        """
        return self.messages[-window_size:]

    def clear_conversation(self):
        """Clear chat messages but keep the user profile."""
        self.messages = []

    def clear_all(self):
        """Reset everything — messages and profile."""
        self.messages = []
        self.user_profile = {
            "name": None,
            "interests": [],
            "goals": [],
            "preferences": [],
        }

    # ------------------------------------------------------------------ #
    #  User Profile (Adaptive Memory)
    # ------------------------------------------------------------------ #

    def _extract_preferences(self, text):
        """Auto-extract user preferences from their messages.

        Uses simple keyword matching to learn about the user.
        This runs every time the user sends a message.

        Args:
            text: the user's message
        """
        text_lower = text.lower()

        # --- Detect name ---
        name_triggers = ["my name is ", "i'm ", "i am ", "call me "]
        for trigger in name_triggers:
            if trigger in text_lower:
                # Extract the word(s) right after the trigger
                start = text_lower.index(trigger) + len(trigger)
                # Take the rest of the sentence (up to punctuation)
                remaining = text[start:].strip()
                # Get first 1-3 words as the name
                name_parts = []
                for word in remaining.split():
                    clean = word.strip(".,!?;:'\"")
                    if clean:
                        name_parts.append(clean)
                    if len(name_parts) >= 2:
                        break
                if name_parts:
                    self.user_profile["name"] = " ".join(name_parts).title()
                break

        # --- Detect interests ---
        interest_triggers = [
            "i like ", "i love ", "i enjoy ", "interested in ",
            "i'm into ", "fan of ", "passionate about ",
        ]
        for trigger in interest_triggers:
            if trigger in text_lower:
                start = text_lower.index(trigger) + len(trigger)
                interest = text[start:].split(".")[0].split(",")[0].strip()
                interest = interest.strip(".,!?;:'\"")
                if interest and interest not in self.user_profile["interests"]:
                    self.user_profile["interests"].append(interest)

        # --- Detect goals ---
        goal_triggers = [
            "i want to ", "my goal is ", "i'm trying to ",
            "i need to ", "i plan to ", "i hope to ",
        ]
        for trigger in goal_triggers:
            if trigger in text_lower:
                start = text_lower.index(trigger) + len(trigger)
                goal = text[start:].split(".")[0].split(",")[0].strip()
                goal = goal.strip(".,!?;:'\"")
                if goal and goal not in self.user_profile["goals"]:
                    self.user_profile["goals"].append(goal)

    def update_profile(self, key, value):
        """Manually update a profile field.

        Args:
            key: profile field name (name, interests, goals, preferences)
            value: the value to set (string for name, string to append for lists)
        """
        if key == "name":
            self.user_profile["name"] = value
        elif key in ("interests", "goals", "preferences"):
            if value not in self.user_profile[key]:
                self.user_profile[key].append(value)

    def get_profile_summary(self):
        """Return a formatted summary of what we know about the user.

        Returns:
            A human-readable string of user preferences, or empty string
            if we haven't learned anything yet.
        """
        parts = []

        if self.user_profile["name"]:
            parts.append(f"Name: {self.user_profile['name']}")

        if self.user_profile["interests"]:
            items = ", ".join(self.user_profile["interests"])
            parts.append(f"Interests: {items}")

        if self.user_profile["goals"]:
            items = ", ".join(self.user_profile["goals"])
            parts.append(f"Goals: {items}")

        if self.user_profile["preferences"]:
            items = ", ".join(self.user_profile["preferences"])
            parts.append(f"Preferences: {items}")

        return "\n".join(parts)

    def get_profile_for_prompt(self):
        """Return profile info formatted for injection into the AI prompt.

        Returns:
            A string to include in the system prompt, or empty string
            if no profile data exists yet.
        """
        summary = self.get_profile_summary()
        if not summary:
            return ""
        return (
            "\n\n--- USER PROFILE (adapt your responses to this) ---\n"
            f"{summary}\n"
            "--- END PROFILE ---"
        )
