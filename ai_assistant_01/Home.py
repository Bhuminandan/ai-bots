import streamlit as st
from utils.helpers import Helpers
helpers = Helpers()
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS



st.set_page_config(page_title="Chatbot App", layout="centered")

# Initialize session state
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step 1: Show input form first
if not st.session_state.chat_started:
    st.title("Welcome to Chatbot")

    with st.form("user_info"):
        name = st.text_input("Your name")
        pdfs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
        submitted = st.form_submit_button("Start Chat")

        with st.spinner("Processing PDFs..."):
            if submitted and name and pdfs:
                # Process PDFs
                documents = helpers.process_pdfs(pdfs)
                submitted = False  # Reset submitted to avoid reprocessing
                # Initialize embeddings and vector store
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                vector_store = FAISS.from_documents(documents, embeddings)

                # Save vector store locally
                vector_store.save_local("vector_store")
                st.session_state.vector_store = vector_store


                # Save user info and chat history
                st.session_state.name = name
                st.session_state.chat_started = True
                st.session_state.chat_history = []

                st.success("Chat started successfully!")

                st.rerun()  # Rerun to show chat interface
            elif submitted:
                st.error("Please enter your name and upload at least one PDF.")
                
# Step 2: Show chat interface
else:
    st.title(f"Chat with Assistant — {st.session_state.name}")

    # Show chat history (chat-style UI)
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input at bottom
    user_message = st.chat_input("Type your message...")

    if user_message:
        # Save user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        # Bot response (mock)
        response = f"Hello {st.session_state.name}, you said: {user_message}"
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    # # Reset option
    # if st.button("🔁 Reset Chat"):
    #     for key in ["chat_started", "chat_history", "name", "email"]:
    #         st.session_state.pop(key, None)
    #     st.rerun()
