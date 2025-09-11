
import streamlit as st
from huggingface_hub import InferenceClient
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Multimodal Chat App",
    page_icon="💬",
    layout="wide",
)

st.title("Multimodal Chatbot UI")
st.markdown("---")

# --- UI Elements ---

# Model selection dropdown
model_options = ("mistralai/Mistral-7B-Instruct-v0.1", "mistralai/Mistral-7B-Instruct-v0.2", "mistralai/Mistral-7B-Instruct-v0.3")
selected_model = st.sidebar.selectbox("Select a model:", model_options)

# Clear Chat History button
def clear_chat_history():
    st.session_state.messages = []

st.sidebar.button("Clear Chat History", on_click=clear_chat_history)
st.sidebar.markdown("---")

# Input text box for user queries
user_input = st.chat_input("Ask me anything...")

# --- Conversation and Logic ---

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Process user input and display AI response
if user_input:
    # Display user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate a response using the selected model
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                # --- Paste your API key here ---
                HF_TOKEN = Your_HF_Token
                # ------------------------------

                client = InferenceClient(
                    model=selected_model,
                    token=HF_TOKEN
                )

                # Prepare messages in the format expected by the API
                messages = [
                    {"role": "system", "content": "You are a helpful and Knowledgeable assistance."},
                    {"role": "user", "content": user_input}
                ]

                # Make the API call with streaming enabled
                response = client.chat_completion(messages=messages, max_tokens=300, stream=True)

                # Stream the response to the user's chat window
                full_response = ""
                for chunk in response:
                    full_response += chunk.choices[0].delta.content
                    st.markdown(full_response)
            
            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            else:
                # Add the full response to chat history after generation is complete
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Export Conversation ---

# Generate conversation text
if st.session_state.messages:
    conversation_text = ""
    for message in st.session_state.messages:
        role = "User" if message["role"] == "user" else "AI"
        conversation_text += f"**{role}:** {message['content']}\n\n"
    
    # Create export button
    st.markdown("---")
    st.download_button(
        label="Download Conversation",
        data=conversation_text.strip(),
        file_name="conversation.txt",
        mime="text/plain"

    )
