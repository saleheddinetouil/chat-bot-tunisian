
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set page config for a wider layout
st.set_page_config(page_title="Tunisian Chatbot", page_icon="🤖", layout="wide")

@st.cache_resource  # Cache the model and tokenizer for faster loading
def load_model_and_tokenizer():
    """Loads the pre-trained Arabic GPT-2 model and tokenizer."""
    model_name = "aubmindlab/bert-base-arabertv2"  # Use a suitable Arabic model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

# Load the model and tokenizer
model, tokenizer = load_model_and_tokenizer()

# Initialize chat history (store in session state to persist across reruns)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Streamlit App UI ---
st.title("🇹🇳  Tunisian Chatbot  🤖")
st.write("Interact with the chatbot in Tunisian dialect!")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("You:")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate chatbot response
    prompt = "".join([f"{'Human: ' if msg['role'] == 'user' else 'Chatbot: '}{msg['content']}\n" 
                     for msg in st.session_state.chat_history])
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_length=128, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Add chatbot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response.split("Chatbot: ")[-1].strip()})

    # Display chatbot response
    with st.chat_message("assistant"):
        st.write(response.split("Chatbot: ")[-1].strip()) 
