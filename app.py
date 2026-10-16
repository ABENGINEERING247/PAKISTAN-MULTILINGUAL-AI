import os
import streamlit as st
from dotenv import load_dotenv
from assistant_core import get_response, MODES, LANGUAGES, suggested_prompts

load_dotenv()
st.set_page_config(page_title="Pakistan Multilingual AI Assistant", page_icon="🇵🇰", layout="wide")

def env_default(key, fallback=""):
    return os.getenv(key, fallback)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Demo"
if "language" not in st.session_state:
    st.session_state.language = "Urdu"
if "model" not in st.session_state:
    st.session_state.model = env_default("OPENAI_MODEL", "gpt-4o-mini")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 1.5rem;}
.hero {padding: 1.5rem; border-radius: 18px; background: linear-gradient(120deg,#064e3b,#166534,#14532d); color:white; margin-bottom:1rem;}
.hero h1 {color:white; margin:0;}
.small-muted {color: #64748b; font-size: .9rem;}
div[data-testid="stChatMessage"] {border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🇵🇰 Assistant Settings")
    st.session_state.mode = st.radio("Operating mode", MODES, index=MODES.index(st.session_state.mode))
    st.session_state.language = st.selectbox("Response language", LANGUAGES, index=LANGUAGES.index(st.session_state.language))
    st.session_state.model = st.text_input("Model name (API mode)", value=st.session_state.model)
    st.caption("API keys are read from environment variables / Streamlit Secrets. Never paste keys into chat.")
    st.divider()
    st.subheader("What I can help with")
    st.markdown("- Urdu, English, and Roman Urdu\n- Learning and technical guidance\n- Drafting and summarizing\n- Pakistan-focused general information\n- Coding and productivity")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("For important legal, medical, financial, or emergency matters, verify with qualified professionals or official sources.")

st.markdown("""
<div class="hero">
  <h1>Pakistan Multilingual AI Assistant</h1>
  <p>ایک مددگار AI اسسٹنٹ — Urdu • English • Roman Urdu</p>
  <p>Ask questions, learn, draft documents, and solve everyday problems.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([3,1])
with left:
    st.subheader("Your AI conversation")
with right:
    st.metric("Mode", st.session_state.mode)
    st.metric("Messages", len(st.session_state.messages))

if not st.session_state.messages:
    st.info("Start with a suggestion or write your question below.")
    cols = st.columns(2)
    prompts = suggested_prompts(st.session_state.language)
    for i, prompt in enumerate(prompts):
        with cols[i % 2]:
            if st.button(prompt, key=f"suggest_{i}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"]=="user" else "🇵🇰"):
        st.markdown(message["content"])

pending = st.session_state.pop("pending_prompt", None)
user_prompt = st.chat_input("اپنا سوال لکھیں / Type your question / Roman Urdu mein likhein…")
if pending:
    user_prompt = pending

if user_prompt:
    st.session_state.messages.append({"role":"user","content":user_prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_prompt)
    with st.chat_message("assistant", avatar="🇵🇰"):
        with st.spinner("Preparing your answer…"):
            try:
                answer, source_mode = get_response(
                    messages=st.session_state.messages,
                    mode=st.session_state.mode,
                    language=st.session_state.language,
                    model=st.session_state.model,
                )
                st.markdown(answer)
                if source_mode == "Demo":
                    st.caption("Demo mode · Responses are illustrative and may be incomplete.")
                st.session_state.messages.append({"role":"assistant","content":answer})
            except Exception as exc:
                st.error(f"Could not generate a response: {exc}")
                st.info("Check your API key and model settings, or switch to Demo mode.")
st.caption("Prototype foundation for a professional service. Add official-source retrieval, authentication, usage limits, and persistent storage before public commercial launch.")
