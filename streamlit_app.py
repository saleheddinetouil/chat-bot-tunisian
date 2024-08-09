import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set page config for a wider layout
st.set_page_config(page_title="Tunisian Chatbot", page_icon="🤖", layout="wide")

# Function to query Gemini Pro
def query_gemini_pro(prompt):
    """Queries Google Gemini Pro and returns the response."""
    import google.generativeai as palm
    palm.configure(api_key="AIzaSyDvMoNqBLBFeIjT_OeUqirKH5SO6n8FR8E")  # Replace with your actual API key

    completion = palm.generate_text(
        model="models/gemini-pro",
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=128,
    )
    return completion.result

@st.cache_resource  # Cache the model and tokenizer for faster loading
def load_model_and_tokenizer():
    """Loads the pre-trained Arabic GPT-2 model and tokenizer (fallback)."""
    model_name = "aubmindlab/bert-base-arabertv2"  
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

# Load the fallback model and tokenizer
model, tokenizer = load_model_and_tokenizer()

# Initialize chat history (store in session state to persist across reruns)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Streamlit App UI ---
st.title("🇹🇳  Tunisian Chatbot  🤖")
st.write("Interact with the chatbot in Tunisian dialect! (Powered by Gemini Pro)")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("You:")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate chatbot response using Gemini Pro
    prompt = "".join([f"{'Human: ' if msg['role'] == 'user' else 'Chatbot: '}{msg['content']}\n" 
                     for msg in st.session_state.chat_history])

    try:
        response = query_gemini_pro(prompt)
    except Exception as e:
        st.error(f"Error querying Gemini Pro: {e}")
        # Fallback to the Arabic GPT-2 model
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_length=128, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Add chatbot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response.split("Chatbot: ")[-1].strip()})

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response.split("Chatbot: ")[-1].strip())
