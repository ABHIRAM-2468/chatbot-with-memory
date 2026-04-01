"""
app.py — Main Streamlit Application (Enhanced)
================================================
ChatGPT-style UI with:
- Dual-thinking modes (Normal / Anti-Gravity)
- Adaptive memory (learns your name, interests, goals)
- Voice input (speech-to-text)
- Export chat as TXT or PDF
- Theme switcher (Dark / Light / Sunset / Ocean)
- Persistent chat history
"""

import streamlit as st
from memory import MemoryManager
from llm import get_response
import chat_history
import export_chat
import config

# ------------------------------------------------------------------ #
#  Page Configuration (must be first Streamlit call)
# ------------------------------------------------------------------ #

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="centered",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
#  Theme Definitions
# ------------------------------------------------------------------ #

THEMES = {
    "🌑 Dark (Default)": {
        "bg": "linear-gradient(135deg, #0E1117 0%, #1A1D23 50%, #0E1117 100%)",
        "sidebar_bg": "linear-gradient(180deg, #1A1D23 0%, #0E1117 100%)",
        "primary": "#6C63FF",
        "user_bubble": "rgba(108,99,255,0.15)",
        "user_border": "rgba(108,99,255,0.4)",
        "ai_bubble": "rgba(255,255,255,0.05)",
        "ai_border": "rgba(255,255,255,0.1)",
        "text": "#FAFAFA",
    },
    "🌊 Ocean": {
        "bg": "linear-gradient(135deg, #0A1628 0%, #0D2137 50%, #0A1628 100%)",
        "sidebar_bg": "linear-gradient(180deg, #0D2137 0%, #0A1628 100%)",
        "primary": "#00B4D8",
        "user_bubble": "rgba(0,180,216,0.15)",
        "user_border": "rgba(0,180,216,0.4)",
        "ai_bubble": "rgba(255,255,255,0.05)",
        "ai_border": "rgba(255,255,255,0.1)",
        "text": "#FAFAFA",
    },
    "🌅 Sunset": {
        "bg": "linear-gradient(135deg, #1A0A0A 0%, #2D1B1B 50%, #1A0A0A 100%)",
        "sidebar_bg": "linear-gradient(180deg, #2D1B1B 0%, #1A0A0A 100%)",
        "primary": "#FF6B6B",
        "user_bubble": "rgba(255,107,107,0.15)",
        "user_border": "rgba(255,107,107,0.4)",
        "ai_bubble": "rgba(255,255,255,0.05)",
        "ai_border": "rgba(255,255,255,0.1)",
        "text": "#FAFAFA",
    },
    "☀️ Light": {
        "bg": "linear-gradient(135deg, #F0F2F6 0%, #FFFFFF 50%, #F0F2F6 100%)",
        "sidebar_bg": "linear-gradient(180deg, #FFFFFF 0%, #F0F2F6 100%)",
        "primary": "#6C63FF",
        "user_bubble": "rgba(108,99,255,0.1)",
        "user_border": "rgba(108,99,255,0.3)",
        "ai_bubble": "rgba(0,0,0,0.03)",
        "ai_border": "rgba(0,0,0,0.1)",
        "text": "#0E1117",
    },
}


def apply_theme(theme_name):
    """Inject CSS for the selected theme."""
    t = THEMES.get(theme_name, THEMES["🌑 Dark (Default)"])
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        * {{ font-family: 'Inter', sans-serif !important; }}

        .stApp {{
            background: {t['bg']};
            color: {t['text']};
        }}

        section[data-testid="stSidebar"] {{
            background: {t['sidebar_bg']};
            border-right: 1px solid rgba(128,128,128,0.2);
        }}

        section[data-testid="stSidebar"] * {{
            color: {t['text']} !important;
        }}

        .stChatMessage {{
            border-radius: 14px;
            margin-bottom: 10px;
            padding: 4px;
        }}

        .stChatInputContainer > div {{
            border-radius: 14px;
            border: 1.5px solid {t['primary']} !important;
            background: rgba(128,128,128,0.05) !important;
        }}

        .stButton > button {{
            border-radius: 8px;
            border: 1px solid {t['primary']};
            background: transparent;
            color: {t['text']};
            font-weight: 500;
            transition: all 0.25s ease;
        }}
        .stButton > button:hover {{
            background: {t['primary']};
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(108,99,255,0.35);
        }}

        .mode-badge {{
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .mode-normal  {{ background: linear-gradient(135deg, #00B4D8, #0077B6); color: white; }}
        .mode-antigravity {{ background: linear-gradient(135deg, #6C63FF, #E040FB); color: white; }}

        .profile-card {{
            background: rgba(108,99,255,0.08);
            border: 1px solid rgba(108,99,255,0.25);
            border-radius: 10px;
            padding: 14px;
            line-height: 1.7;
        }}

        .feature-banner {{
            background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(224,64,251,0.1));
            border: 1px solid rgba(108,99,255,0.3);
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 16px;
            font-size: 0.88em;
        }}

        h1, h2, h3 {{
            color: {t['text']} !important;
        }}

        .section-label {{
            font-size: 0.78em;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            opacity: 0.55;
            margin-bottom: 6px;
        }}

        .stRadio [data-testid="stMarkdownContainer"] p {{
            font-size: 0.92em;
        }}

        .stDownloadButton > button {{
            border-radius: 8px;
            border: 1px solid {t['primary']};
            background: linear-gradient(135deg, {t['primary']}22, {t['primary']}11);
            color: {t['text']};
            font-weight: 500;
            transition: all 0.25s ease;
            width: 100%;
        }}
        .stDownloadButton > button:hover {{
            background: {t['primary']};
            color: white;
            transform: translateY(-1px);
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Session State Initialization
# ------------------------------------------------------------------ #

def init_session():
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryManager()
    if "mode" not in st.session_state:
        st.session_state.mode = config.DEFAULT_MODE
    if "theme" not in st.session_state:
        st.session_state.theme = "🌑 Dark (Default)"
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""


init_session()
apply_theme(st.session_state.theme)

# ------------------------------------------------------------------ #
#  SIDEBAR
# ------------------------------------------------------------------ #

with st.sidebar:
    # Branding
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 5px 0;">
        <span style="font-size:2.2em;">🧠</span>
        <h2 style="margin:4px 0 2px 0; font-size:1.3em;">Anti-Gravity AI</h2>
        <p style="font-size:0.78em; opacity:0.5; margin:0;">Next-gen chatbot with memory</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ---- Mode Selection ----
    st.markdown('<p class="section-label">⚙️ Thinking Mode</p>', unsafe_allow_html=True)
    mode = st.radio(
        "Choose mode:",
        options=["Normal", "Anti-Gravity"],
        index=0 if st.session_state.mode == "Normal" else 1,
        help="**Normal** — helpful answers.\n\n**Anti-Gravity** — practical + creative twist!",
        label_visibility="collapsed",
    )
    st.session_state.mode = mode

    badge_class = "mode-normal" if mode == "Normal" else "mode-antigravity"
    badge_label = "🧱 Normal Mode" if mode == "Normal" else "🚀 Anti-Gravity Mode"
    st.markdown(
        f'<span class="mode-badge {badge_class}">{badge_label}</span>',
        unsafe_allow_html=True,
    )

    st.divider()

    # ---- Theme Switcher ----
    st.markdown('<p class="section-label">🎨 Theme</p>', unsafe_allow_html=True)
    theme = st.selectbox(
        "Theme",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
        label_visibility="collapsed",
    )
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()

    st.divider()

    # ---- Voice Input ----
    st.markdown('<p class="section-label">🎙️ Voice Input</p>', unsafe_allow_html=True)

    voice_available = False
    try:
        from audio_recorder_streamlit import audio_recorder
        voice_available = True
    except ImportError:
        pass

    if voice_available:
        st.caption("Click the mic, speak, and your words appear in the chat box.")
        audio_bytes = audio_recorder(
            text="",
            recording_color="#6C63FF",
            neutral_color="#555",
            icon_size="2x",
            pause_threshold=2.5,
        )
        if audio_bytes:
            try:
                import speech_recognition as sr
                import io

                recognizer = sr.Recognizer()
                audio_file = io.BytesIO(audio_bytes)
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                st.session_state.voice_text = text
                st.success(f"Heard: *{text}*")
            except Exception as e:
                st.warning(f"Could not transcribe: {e}")
    else:
        st.info("Install `audio-recorder-streamlit` and `SpeechRecognition` to enable voice input.")

    st.divider()

    # ---- User Profile Display ----
    profile_summary = st.session_state.memory.get_profile_summary()
    if profile_summary:
        st.markdown('<p class="section-label">👤 Your Profile</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="profile-card">{profile_summary.replace(chr(10), "<br>")}</div>',
            unsafe_allow_html=True,
        )
        st.divider()

    # ---- Export & Actions ----
    st.markdown('<p class="section-label">🛠️ Actions</p>', unsafe_allow_html=True)

    messages = st.session_state.memory.get_history()
    profile = st.session_state.memory.user_profile

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.memory.clear_conversation()
            st.session_state.voice_text = ""
            st.rerun()
    with col2:
        if st.button("💾 Save Chat", use_container_width=True):
            if messages:
                fname = chat_history.save_chat(messages, profile)
                st.success(f"Saved!")
            else:
                st.warning("Nothing to save yet!")

    # Export as TXT
    if messages:
        txt_content = export_chat.export_as_text(messages, profile)
        st.download_button(
            label="📄 Export as TXT",
            data=txt_content.encode("utf-8"),
            file_name=f"chat_export.txt",
            mime="text/plain",
            use_container_width=True,
        )

        # Export as PDF
        try:
            pdf_bytes = export_chat.export_as_pdf(messages, profile)
            st.download_button(
                label="📕 Export as PDF",
                data=pdf_bytes,
                file_name="chat_export.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception:
            pass

    st.divider()

    # ---- Chat History Browser ----
    st.markdown('<p class="section-label">📂 Saved Chats</p>', unsafe_allow_html=True)
    saved_chats = chat_history.list_chats()

    if saved_chats:
        for chat_info in saved_chats[:8]:
            col_load, col_del = st.columns([3, 1])
            label = chat_info["filename"].replace("chat_", "").replace(".json", "")
            with col_load:
                if st.button(f"📄 {label}", key=f"load_{chat_info['filename']}",
                             use_container_width=True):
                    data = chat_history.load_chat(chat_info["filename"])
                    if data:
                        st.session_state.memory.messages = data["messages"]
                        if "user_profile" in data:
                            st.session_state.memory.user_profile = data["user_profile"]
                        st.rerun()
            with col_del:
                if st.button("✕", key=f"del_{chat_info['filename']}"):
                    chat_history.delete_chat(chat_info["filename"])
                    st.rerun()
    else:
        st.caption("No saved chats yet.")

    st.divider()
    st.caption("Built with ❤️ · Streamlit + OpenAI")

# ------------------------------------------------------------------ #
#  MAIN CHAT AREA
# ------------------------------------------------------------------ #

# Header
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown(f"## {config.APP_TITLE}")
with col_badge:
    st.markdown(
        f'<div style="padding-top:14px"><span class="mode-badge '
        f'{"mode-normal" if st.session_state.mode == "Normal" else "mode-antigravity"}">'
        f'{"🧱 Normal" if st.session_state.mode == "Normal" else "🚀 Anti-Gravity"}'
        f'</span></div>',
        unsafe_allow_html=True,
    )

# Feature banner (shown once when no messages)
if not st.session_state.memory.get_history():
    st.markdown("""
    <div class="feature-banner">
        ✨ <b>Tips:</b>
        &nbsp;Switch to <b>Anti-Gravity</b> mode for creative dual answers &nbsp;·&nbsp;
        Tell me your name and interests — I'll remember! &nbsp;·&nbsp;
        Use the mic 🎙️ for voice input &nbsp;·&nbsp;
        Export chats as TXT or PDF
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.memory.get_history():
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Welcome message
if not st.session_state.memory.get_history():
    with st.chat_message("assistant", avatar="🤖"):
        if st.session_state.mode == "Anti-Gravity":
            st.markdown(
                "🚀 **Anti-Gravity mode ON!**\n\n"
                "Every answer I give has two layers:\n"
                "- 🧱 **Ground Floor** — the practical, solid answer\n"
                "- 🚀 **Gravity Break** — a creative twist that'll surprise you\n\n"
                "Tell me your name and what you're working on — I'll personalize everything for you. What's on your mind?"
            )
        else:
            st.markdown(
                "👋 **Hey! I'm Anti-Gravity AI.**\n\n"
                "I adapt to you as we talk — tell me your name, interests, or goals. "
                "I'll remember and personalize every response.\n\n"
                "What can I help you with today?"
            )

# ---- Chat Input (typed or voice) ----
voice_prefill = st.session_state.voice_text
placeholder = f'🎙️ Voice ready: "{voice_prefill}" — press Enter to send' if voice_prefill else "Type your message..."

user_input = st.chat_input(placeholder)

# Use voice text if no typed input
if not user_input and voice_prefill:
    user_input = voice_prefill
    st.session_state.voice_text = ""

if user_input:
    st.session_state.voice_text = ""  # Clear voice buffer

    # Show user's message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Store in memory
    st.session_state.memory.add_message("user", user_input)

    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            context = st.session_state.memory.get_context_window(config.CONTEXT_WINDOW)
            profile_ctx = st.session_state.memory.get_profile_for_prompt()
            response = get_response(
                messages=context,
                mode=st.session_state.mode,
                profile_context=profile_ctx,
            )
            st.markdown(response)

    # Store response
    st.session_state.memory.add_message("assistant", response)

    # Auto-save after every exchange if there are 10+ messages
    if len(st.session_state.memory.get_history()) % 10 == 0:
        chat_history.save_chat(
            st.session_state.memory.get_history(),
            st.session_state.memory.user_profile,
        )
