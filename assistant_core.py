import os
from typing import List, Dict, Tuple

MODES = ["Demo", "API"]
LANGUAGES = ["Urdu", "English", "Roman Urdu", "Auto-detect"]

SYSTEM_PROMPT = """You are Pakistan Multilingual AI Assistant, a helpful, respectful and practical assistant for users in Pakistan.
Support Urdu, English and Roman Urdu. Follow the selected response language. Use clear, accessible language.
For Pakistan-specific legal, tax, government, medical, financial, and current affairs questions, do not invent facts, laws, contacts, fees, or deadlines. Explain uncertainty and recommend checking relevant official sources.
Do not claim to have browsed the web or verified current facts unless a retrieval tool is actually connected.
Do not request passwords, API keys, CNIC numbers, or unnecessary sensitive personal data. Refuse harmful or illegal instructions and offer safe alternatives.
Structure answers with headings and steps when useful. For consequential decisions, state limitations and encourage qualified human review."""

def suggested_prompts(language: str) -> List[str]:
    prompts = {
        "Urdu": ["مجھے Python سیکھنے کا منصوبہ بنائیں", "ایک رسمی درخواست لکھیں", "مصنوعی ذہانت آسان الفاظ میں سمجھائیں", "میرے کاروبار کے لیے آئیڈیاز دیں"],
        "English": ["Create a Python learning plan", "Draft a formal application letter", "Explain AI in simple terms", "Suggest ideas for a small business"],
        "Roman Urdu": ["Mujhe Python seekhnay ka plan dein", "Aik formal application likh dein", "AI ko asaan alfaaz mein samjhaein", "Chotay business ke ideas dein"],
        "Auto-detect": ["Create a Python learning plan", "Draft a formal application letter", "Explain AI in simple terms", "Suggest ideas for a small business"],
    }
    return prompts.get(language, prompts["English"])

def demo_response(user_text: str, language: str) -> str:
    text = user_text.lower()
    if any(word in text for word in ["python", "پائتھن", "coding", "programming"]):
        if language == "Urdu":
            return """### Python سیکھنے کا عملی منصوبہ\n1. **ہفتہ 1:** variables، data types، input/output اور operators۔\n2. **ہفتہ 2:** if/else، loops، lists، dictionaries اور functions۔\n3. **ہفتہ 3:** files، exceptions، modules اور بنیادی OOP۔\n4. **ہفتہ 4:** Pandas، charts اور ایک چھوٹا Streamlit project۔\n\nروزانہ 45–60 منٹ مشق کریں۔ ہر موضوع کے بعد ایک چھوٹا project بنائیں۔"""
        if language == "Roman Urdu":
            return """### Python ka practical learning plan\n1. **Week 1:** variables, data types, input/output aur operators.\n2. **Week 2:** if/else, loops, lists, dictionaries aur functions.\n3. **Week 3:** files, exceptions, modules aur basic OOP.\n4. **Week 4:** Pandas, charts aur aik chhota Streamlit project.\n\nRozana 45–60 minutes practice karein aur har topic ke baad mini project banayein."""
        return """### Practical Python learning plan\n1. **Week 1:** Variables, data types, input/output, and operators.\n2. **Week 2:** Conditionals, loops, lists, dictionaries, and functions.\n3. **Week 3:** Files, exceptions, modules, and basic OOP.\n4. **Week 4:** Pandas, charts, and a small Streamlit project.\n\nPractice for 45–60 minutes daily and build a mini-project after each topic."""
    if any(word in text for word in ["letter", "application", "درخواست", "darkhwast"]):
        return """### Formal letter template\n\n**Subject: [Write the subject here]**\n\nRespected Sir/Madam,\n\nWith due respect, I would like to state that [briefly explain your request and relevant details]. I kindly request you to consider my application.\n\nThank you for your time and consideration.\n\nYours faithfully,  \n[Your Name]  \n[Designation / Department]  \n[Date]\n\n*Replace the bracketed fields with accurate details before sending.*"""
    if any(word in text for word in ["business", "کاروبار", "karobar"]):
        return """### Practical small-business idea checklist\n- Identify one specific customer problem.\n- Interview 10 potential customers before investing heavily.\n- Estimate setup costs, monthly expenses, pricing, and break-even sales.\n- Test demand with a small pilot or pre-orders.\n- Keep business records and check applicable Pakistani registration, tax, and licensing requirements with official sources or a qualified adviser.\n\nTell me your city, budget range, skills, and preferred industry (without sharing sensitive personal details) for a more tailored shortlist."""
    if any(word in text for word in ["ai", "مصنوعی ذہانت"]):
        return """### Artificial intelligence, simply explained\nArtificial intelligence (AI) is software that performs tasks such as understanding language, recognizing images, finding patterns, or generating content. A generative AI model predicts and creates outputs based on patterns learned during training. AI can make mistakes, so verify important information, especially for legal, medical, financial, and government matters."""
    if language == "Urdu":
        return """میں ڈیمو موڈ میں کام کر رہا ہوں، اس لیے میرا جواب محدود اور مثال کے طور پر ہے۔ آپ اپنا سوال مزید واضح لکھیں، یا API موڈ فعال کریں تاکہ منسلک language model سے جواب حاصل کیا جا سکے۔ اہم معلومات کو مستند ذرائع سے ضرور چیک کریں۔"""
    if language == "Roman Urdu":
        return """Main Demo mode mein hoon, is liye mera jawab limited aur illustrative hai. Apna sawal mazeed wazeh likhein, ya connected language model se jawab ke liye API mode use karein. Ahm maloomat ko trusted sources se verify zaroor karein."""
    return """I am running in Demo mode, so this response is limited and illustrative. Please add more detail to your question, or switch to API mode to use a connected language model. Verify important information with trusted sources."""

def get_response(messages: List[Dict[str, str]], mode: str, language: str, model: str) -> Tuple[str, str]:
    user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    if mode == "Demo":
        return demo_response(user_text, language), "Demo"

    api_key = st_secret_or_env("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured in Streamlit Secrets or environment variables.")
    if not model.strip():
        raise RuntimeError("Enter a valid model name in the sidebar.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("The openai package is not installed. Install requirements.txt.") from exc

    client = OpenAI(api_key=api_key)
    language_instruction = {
        "Urdu": "Respond in Urdu script.",
        "English": "Respond in English.",
        "Roman Urdu": "Respond in Roman Urdu (Urdu written using Latin letters).",
        "Auto-detect": "Respond in the language used by the user; support Urdu, English and Roman Urdu.",
    }.get(language, "Respond in the language used by the user.")
    api_messages = [{"role":"system","content":SYSTEM_PROMPT + "\n" + language_instruction}]
    # Keep recent context bounded to reduce token use and avoid unbounded prompts.
    for msg in messages[-16:]:
        if msg.get("role") in ("user", "assistant") and isinstance(msg.get("content"), str):
            api_messages.append({"role":msg["role"],"content":msg["content"][:12000]})
    response = client.chat.completions.create(
        model=model.strip(),
        messages=api_messages,
        temperature=0.4,
        max_tokens=1200,
        timeout=45,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")
    return content, "API"

def st_secret_or_env(key: str) -> str:
    value = os.getenv(key, "")
    try:
        import streamlit as st
        value = st.secrets.get(key, value)
    except Exception:
        pass
    return str(value or "").strip()
