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
    st.session_state.model = env_default("OPENAI_MODEL", "gpt-6-luna")
if "temperature" not in st.session_state:
    st.session_state.temperature = 1.0

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
    
    # Model selection including GPT-6 Luna
    model_options = ["gpt-6-luna", "gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet"]
    current_model = st.session_state.model
    if current_model not in model_options:
        model_options.append(current_model)
    st.session_state.model = st.selectbox("Model name", model_options, index=model_options.index(current_model))
    
    # Temperature slider set to 1.0 default
    st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=st.session_state.temperature, step=0.1)
    
    st.caption("API keys are read from environment variables / Streamlit Secrets. Never paste keys into chat.")
    st.divider()
    st.subheader("What I can help with")
    st.markdown("- Urdu, English, and Roman Urdu\n- Learning and technical guidance\n- Drafting and summarizing\n- Pakistan-focused general information\n- Coding and productivity")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("**Developed & Designed by:**<br>Engr. Bilal Mehmood", unsafe_allow_html=True)
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
    st.metric("Model", st.session_state.model)

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
                # Pass temperature if supported by assistant_core, with fallback
                try:
                    answer, source_mode = get_response(
                        messages=st.session_state.messages,
                        mode=st.session_state.mode,
                        language=st.session_state.language,
                        model=st.session_state.model,
                        temperature=st.session_state.temperature,
                    )
                except TypeError:
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

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b;'>Prototype foundation for a professional service. Developed and designed by <b>Engr. Bilal Mehmood</b>.</div>", unsafe_allow_html=True)
