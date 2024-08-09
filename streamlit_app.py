import streamlit as st
import os

# Set page config for a wider layout
st.set_page_config(page_title="Darija Chatbot", page_icon="🤖", layout="wide")

# Get API key from environment variable
api_key = os.getenv("API")
if api_key is None:
    st.error("Error: GOOGLE_API_KEY environment variable is not set.")
    st.stop()

# Function to query Gemini
def query_gemini(prompt, model_name="models/chat-bison-001"):
    """Queries Google Gemini with the specified model and returns the response."""
    import google.generativeai as palm
    palm.configure(api_key=api_key)

    completion = palm.generate_text(
        model=model_name,
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=128,
    )
    return completion.result

# Initialize chat history (store in session state to persist across reruns)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Streamlit App UI ---
st.title("🇩🇿 Darija Chatbot 🤖")
st.write("Interact with the chatbot in Darija! (Powered by Gemini)")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("You:")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate chatbot response using Gemini
    prompt = "".join([f"{'Human: ' if msg['role'] == 'user' else 'Chatbot: '}{msg['content']}\n" 
                     for msg in st.session_state.chat_history])

    try:
        response = query_gemini(prompt)
    except Exception as e:
        st.error(f"Error querying Gemini: {e}")
        response = "Sorry, I'm having trouble understanding you right now."  # Fallback response

    # Add chatbot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response.split("Chatbot: ")[-1].strip()})

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response.split("Chatbot: ")[-1].strip())
