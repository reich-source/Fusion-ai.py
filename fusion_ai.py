
import streamlit as st
import requests

st.set_page_config(page_title="Fusion AI", layout="wide")
st.title("🤖 Fusion AI: Ultimate Answer Machine")

# Input: API keys
st.sidebar.header("🔐 API Keys")
gpt_key = st.sidebar.text_input("OpenAI GPT-4 Key", type="password")
gemini_key = st.sidebar.text_input("Gemini (Google) Key", type="password")
cohere_key = st.sidebar.text_input("Cohere API Key", type="password")
openrouter_key = st.sidebar.text_input("OpenRouter Key", type="password")

# User question input
query = st.text_area("🧠 Ask your question:", height=100)

# Handle button
if st.button("⚡ Generate Ultimate Answer") and query:
    responses = []

    # OpenAI GPT-4
    if gpt_key:
        try:
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {gpt_key}"},
                json={"model": "gpt-4", "messages": [{"role": "user", "content": query}]}
            )
            responses.append(("GPT-4", r.json()['choices'][0]['message']['content']))
        except: responses.append(("GPT-4", "❌ Error"))

    # Gemini
    if gemini_key:
        try:
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}",
                json={"contents": [{"parts": [{"text": query}]}]}
            )
            responses.append(("Gemini", r.json()['candidates'][0]['content']['parts'][0]['text']))
        except: responses.append(("Gemini", "❌ Error"))

    # Cohere
    if cohere_key:
        try:
            r = requests.post(
                "https://api.cohere.ai/v1/chat",
                headers={"Authorization": f"Bearer {cohere_key}"},
                json={"message": query, "model": "command-r"}
            )
            responses.append(("Cohere", r.json()['text']))
        except: responses.append(("Cohere", "❌ Error"))

    # Mistral via OpenRouter
    if openrouter_key:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {openrouter_key}"},
                json={"model": "mistralai/mixtral-8x7b", "messages": [{"role": "user", "content": query}]}
            )
            responses.append(("Mixtral (OpenRouter)", r.json()['choices'][0]['message']['content']))
        except: responses.append(("Mixtral (OpenRouter)", "❌ Error"))

    # Alek.ai (simulated via GET)
    try:
        alek = requests.get(f"https://alek.ai/api/ask?q={query}")
        responses.append(("Alek.ai", alek.json().get("answer", "❌ No Answer")))
    except: responses.append(("Alek.ai", "❌ Error"))

    # DuckDuckGo Instant Answer
    try:
        ddg = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1")
        abstract = ddg.json().get("Abstract") or ddg.json().get("Answer") or "No instant answer"
        responses.append(("DuckDuckGo", abstract))
    except: responses.append(("DuckDuckGo", "❌ Error"))

    # Display responses
    st.subheader("🔍 Fused Answers:")
    for name, answer in responses:
        st.markdown(f"### 🧠 {name}\n{answer}\n---")
else:
    st.info("Enter a question and press the button to get your answer.")
