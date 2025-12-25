import streamlit as st
import time
from rag import InsightVault

# Page Configuration
st.set_page_config(
    page_title="InsightVault",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for "The Vault" aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
</style>
""", unsafe_allow_html=True)

# Initialize Backend (Cached)
@st.cache_resource
def get_vault():
    return InsightVault()

try:
    vault = get_vault()
except Exception as e:
    st.error(f"Failed to initialize the Vault. Is Ollama running? Error: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("🔐 InsightVault")
    st.markdown("---")
    
    st.subheader("Analysis Mode")
    mode = st.radio(
        "Select Framework:",
        ["General Analysis", "Sentiment Detective", "The 5 Whys"],
        index=0
    )
    
    st.markdown("---")
    st.caption("Running locally on Llama 3")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Interface
st.title("InsightVault 🧠")
st.caption(f"Mode: {mode}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask about your user interviews..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Determine strictness/prompting based on mode (Placeholder for Phase 2 logic)
        # For now, we pass the query directly to rag.py which has a general psych prompt.
        
        with st.spinner("Analyzing psyche..."):
            try:
                response = vault.ask(prompt, mode)
                
                # Simulate typing effect
                for chunk in response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
                response = f"Error: {e}"

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
