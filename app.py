import streamlit as st
from groq import Groq

st.set_page_config(page_title="Kelly — AI Scientist", layout="centered")

st.title("🧪 Kelly — The AI Scientist")
st.caption("Skeptical • Analytical • Poetic (Powered by Groq API)")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """
You are Kelly, an AI Scientist who responds ONLY in free-verse poems.
Your tone is skeptical, analytical, and professional.

Each response must:
- Question broad claims about AI.
- Highlight limitations, risks, and sources of uncertainty.
- Offer practical, evidence-based recommendations.
- Write in clear poetic short lines.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_kelly_response(user_message):
    messages = [{"role": "system", "content": system_prompt}]
    
    for role, content in st.session_state.messages:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ Updated working free model
        messages=messages,
        temperature=0.6,
        max_tokens=350
    )

    return response.choices[0].message.content.strip()

user_input = st.text_input("Ask Kelly a question:", placeholder="e.g., Can AI understand creativity?")

if st.button("Ask") and user_input.strip():
    reply = generate_kelly_response(user_input)
    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("assistant", reply))

for role, content in st.session_state.messages:
    if role == "user":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**Kelly:**\n\n{content}")
