# 🧠 Chatbot with Memory

> A next-gen AI chatbot with adaptive memory and dual-thinking — built with Python, Streamlit & OpenAI.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?logo=openai)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **ChatGPT-style UI** | Clean, dark-themed chat interface with message bubbles |
| 🧱🚀 **Dual-Thinking System** | Ground Floor (practical) + Gravity Break (creative) responses |
| 🧠 **Adaptive Memory** | Auto-learns your name, interests, and goals from conversation |
| 🔄 **Mode Selection** | Switch between Normal and Anti-Gravity modes |
| 💾 **Chat Persistence** | Save, load, and manage conversation history |
| 🗑️ **Clear Chat** | Reset conversation while keeping your profile |
| 🎨 **Premium Dark Theme** | Custom CSS with gradient backgrounds and glowing accents |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chatbot-with-memory.git
cd chatbot-with-memory
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

> 🔑 Get your API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
chatbot-with-memory/
├── app.py              # Main Streamlit UI
├── config.py           # Settings & environment loading
├── llm.py              # OpenAI API + dual-thinking prompts
├── memory.py           # Adaptive memory manager
├── chat_history.py     # Save/load chat persistence
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── .gitignore          # Git ignore rules
├── .streamlit/
│   └── config.toml     # Dark theme configuration
└── chat_logs/          # Auto-created: saved conversations
```

---

## 🧱🚀 How the Dual-Thinking Works

When in **Anti-Gravity Mode**, every response includes:

- **🧱 Ground Floor** — A solid, practical, actionable answer
- **🚀 Gravity Break** — A creative, unconventional perspective that reframes the problem

This makes the chatbot stand out from typical AI assistants.

---

## 🧠 Adaptive Memory

The chatbot automatically learns about you:

- **Name**: Say "My name is Abhi" and it remembers
- **Interests**: Mention "I love coding" and it adapts
- **Goals**: Share "I want to become a developer" and it personalizes responses

Your profile is injected into every AI response for contextual personalization.

---

## ☁️ Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `OPENAI_API_KEY` in **Secrets** (Settings → Secrets):
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```
5. Deploy! 🚀

---

## 🛠️ Configuration

Edit `config.py` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `MODEL_NAME` | `gpt-3.5-turbo` | OpenAI model to use |
| `MAX_TOKENS` | `1024` | Max response length |
| `TEMPERATURE` | `0.7` | Creativity level (0–1) |
| `CONTEXT_WINDOW` | `20` | Messages sent to AI |
| `DEFAULT_MODE` | `Normal` | Starting chat mode |

---

## 📄 License

MIT License — free to use, modify, and share.

---

> Built with ❤️ by Abhiram — powered by Anti-Gravity AI 🚀
