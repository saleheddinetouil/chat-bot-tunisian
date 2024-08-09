import streamlit as st
import os
import google.generativeai as genai

# Set page config for a wider layout
st.set_page_config(page_title="Darija Chatbot", page_icon="🤖", layout="wide")

# Get API key from environment variable
api_key = os.getenv("API")
if api_key is None:
    st.error("Error: GEMINI_API_KEY environment variable is not set.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        "YOU ONLY SPEAK DARIJA : TUNISIAN ALGERIAN MAROCCAN, Use other languages only in explaining in french or english otherwise darija is main."
    ]

# --- Streamlit App UI ---
st.title("🇩🇿 Darija Chatbot 🤖")
st.write("Interact with the chatbot in Darija! (Powered by Gemini)")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message("assistant" if message.startswith("output:") else "user"):
        st.write(message.replace("input:", "").replace("output:", "").strip())

# User input
user_input = st.chat_input("You:")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(f"input:{user_input}")

    # Generate chatbot response using Gemini
    prompt = st.session_state.chat_history.copy()
    prompt.append("output:")
    response = model.generate_content(prompt)

    # Add chatbot response to chat history
    st.session_state.chat_history.append(f"output:{response.text}")

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response.text)
