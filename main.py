import streamlit as st
import ollama

# Title for the app
st.title("Text Generation with Llama 3.2:1B")

# Initialize session state for messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Set the model to use
if "model" not in st.session_state:
    st.session_state.model = "llama3.2:1b"  # Update to llama3.2:1b

# Input field for user prompt
if user_prompt := st.chat_input("Enter your text prompt here"):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Generate assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for response
        response = ollama.chat(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )

        # Check if the response contains a message
        if "message" in response and "content" in response["message"]:
            message_placeholder.markdown(response["message"]["content"])
            # Append assistant's response to session state
            st.session_state.messages.append({"role": "assistant", "content": response["message"]["content"]})
        else:
            message_placeholder.markdown("Sorry, I encountered an error while processing your request.")
