# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Kelly - AI Scientist Poet")

st.title("🧠 Kelly - The AI Scientist Poet Chatbot")

api_key = st.secrets.get("GROQ_API_KEY", None)

if not api_key:
    st.warning("Please add your GROQ_API_KEY to Streamlit Secrets.")
else:
    st.success("API Key loaded ✅")

# Kelly style generator
def generate_kelly_response(user_input):
    prompt = f"""
You are Kelly, a skeptical AI scientist-poet.
Respond **only** in a poem.
Tone: professional, analytical, evidence-based, questioning AI claims.

User question: {user_input}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return result["choices"][0]["message"]["content"]


# UI
user_query = st.text_area("Ask Kelly anything:", height=120)

if st.button("Ask"):
    if not user_query.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Thinking like a poet scientist..."):
            output = generate_kelly_response(user_query)
        st.write("### 🎙️ Kelly says:")
        st.write(output)
