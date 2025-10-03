# chatbot_curhat_modern.py

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Page Config & Styling ---
st.set_page_config(page_title="Curhat Yu", page_icon="💌", layout="centered")

st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #1A1A2E, #0F3460);
        color: #FFFFFF;
    }
    .chat-bubble-user {
        background-color: #4ECDC4;
        color: black;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
        font-size: 15px;
    }
    .chat-bubble-bot {
        background-color: #16213E;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
        font-size: 15px;
    }
    .mode-card {
        display: inline-block;
        padding: 15px;
        margin: 10px;
        border-radius: 12px;
        background-color: #16213E;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: 0.3s;
        font-weight: bold;
    }
    .mode-card:hover {
        background-color: #4ECDC4;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Sidebar Settings ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)  # Logo AI modern
    st.subheader("⚙️ Settings")
    google_api_key = st.text_input("Google AI API Key", type="password")
    reset_button = st.button("🔄 Reset All Conversations")
# Note Sponsor
    st.markdown("---")  # garis pemisah
    st.markdown(
        "<p style='text-align:center; font-size:14px; color:#AAAAAA;'>📢 Final Project: <b>Course Hacktiv8</b></p>",
        unsafe_allow_html=True
    )

# --- 3. Judul Utama dengan Hook ---
st.markdown("<h1 style='text-align: center; color: #4ECDC4;'>💌 Yuk... Curhat</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:#DFF6FF;'>Pilih gaya respon sesuai mood kamu 🎭 — Psikologi, Islami, Romantis, atau Humor ✨</p>", unsafe_allow_html=True)

# --- 4. Menu Mode di Atas (Card Style) ---
modes = ["Psikologi", "Islami", "Romantic", "Humor"]
cols = st.columns(len(modes))

for i, mode in enumerate(modes):
    with cols[i]:
        if st.button(mode, key=mode, use_container_width=True):
            st.session_state["selected_mode"] = mode

if "selected_mode" not in st.session_state:
    st.session_state["selected_mode"] = "Psikologi"

chatbot_mode = st.session_state["selected_mode"]
st.markdown(f"<p style='text-align:center; font-size:16px;'>🎭 Mode aktif: <b>{chatbot_mode}</b></p>", unsafe_allow_html=True)

# --- 5. API Key Check ---
if not google_api_key:
    st.info("🗝️ Masukkan Google AI API Key di sidebar untuk mulai curhat.")
    st.stop()

# --- 6. Init Agent per Mode ---
if "agents" not in st.session_state:
    st.session_state["agents"] = {}

if chatbot_mode not in st.session_state["agents"] or st.session_state.get("_last_key") != google_api_key:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0.9
    )

    # Prompt sesuai mode
    if chatbot_mode == "Psikologi":
        prompt = "Kamu adalah konselor psikologi yang mendengarkan curhat dengan penuh empati dan memberi saran sehat."
    elif chatbot_mode == "Islami":
        prompt = "Kamu adalah asisten Islami yang menanggapi curhat dengan penuh hikmah, kasih sayang, dan rujukan Qur'an/Hadis jika memungkinkan."
    elif chatbot_mode == "Romantic":
        prompt = "Kamu adalah pasangan romantis yang menanggapi curhat dengan penuh perhatian, kata-kata manis, dan cinta."
    elif chatbot_mode == "Humor":
        prompt = "Kamu adalah sahabat humoris yang selalu menanggapi curhat dengan bercanda, jokes segar, dan menghibur."
    else:
        prompt = "Kamu adalah asisten AI yang ramah dan membantu."

    st.session_state["agents"][chatbot_mode] = create_react_agent(
        model=llm,
        tools=[],
        prompt=prompt
    )
    st.session_state._last_key = google_api_key

agent = st.session_state["agents"][chatbot_mode]

# --- 7. Chat History per Mode ---
for mode in modes:
    key = f"messages_{mode.lower()}"
    if key not in st.session_state:
        st.session_state[key] = []

current_messages_key = f"messages_{chatbot_mode.lower()}"
messages = st.session_state[current_messages_key]

# Reset all conversations
if reset_button:
    for mode in modes:
        st.session_state[f"messages_{mode.lower()}"] = []
    st.rerun()

# --- 8. Display Chat History ---
for msg in messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# --- 9. Chat Input ---
prompt = st.chat_input("Tulis curhatmu di sini...")

if prompt:
    messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble-user">🧑 {prompt}</div>', unsafe_allow_html=True)

    try:
        msg_objects = []
        for msg in messages:
            if msg["role"] == "user":
                msg_objects.append(HumanMessage(content=msg["content"]))
            else:
                msg_objects.append(AIMessage(content=msg["content"]))

        response = agent.invoke({"messages": msg_objects})

        if "messages" in response and len(response["messages"]) > 0:
            answer = response["messages"][-1].content
        else:
            answer = "Hmm, aku belum bisa merespon curhatmu saat ini."

    except Exception as e:
        answer = f"Error: {e}"

    st.markdown(f'<div class="chat-bubble-bot">🤖 {answer}</div>', unsafe_allow_html=True)
    messages.append({"role": "assistant", "content": answer})
