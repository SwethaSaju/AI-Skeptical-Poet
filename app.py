import streamlit as st
from groq import Groq

# Streamlit page setup
st.set_page_config(page_title="Kelly — AI Scientist", layout="centered")

st.title("🧪 Kelly — The AI Scientist")
st.caption("Skeptical • Analytical • Poetic (Powered by Groq API)")

# Initialize the Groq API client (reads key from Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# System behavior (defines the poetic Kelly personality)
system_prompt = """
You are Kelly, an AI Scientist who responds ONLY in free-verse poems.
Your tone is skeptical, analytical, and professional.

Each response must:
- Question broad claims about AI.
- Highlight limitations, risks, and sources of uncertainty.
- Offer practical, evidence-based recommendations.
- Write in clear poetic short lines.
"""

# Store chat history between UI refreshes
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_kelly_response(user_message):
    # Build conversation context
    messages = [{"role": "system", "content": system_prompt}]
    
    for role, content in st.session_state.messages:
        messages.append({"role": role, "content": content})
    
    messages.append({"role": "user", "content": user_message})

    # Call Groq model
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
        temperature=0.6,
        max_tokens=350
    )

    return response.choices[0].message.content.strip()

# User input
user_input = st.text_input("Ask Kelly a question:", placeholder="e.g., Can AI understand creativity?")

if st.button("Ask") and user_input.strip():
    reply = generate_kelly_response(user_input)
    
    # Add to chat history
    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("assistant", reply))

# Display conversation history
for role, content in st.session_state.messages:
    if role == "user":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**Kelly:**\n\n{content}")

