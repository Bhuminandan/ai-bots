# Phase 1 imports
import streamlit as st

from dotenv import load_dotenv
load_dotenv()


# Phase 2 imports
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Phase 3 imports
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA


st.title("Real-time Chat with PDF")

# Take Pdf file as input
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if pdf_file is not None:
    # If pdf already exists, delete it
    if os.path.exists("./Research.pdf"):
        os.remove("./Research.pdf")

    # Save the uploaded PDF file to a local path
    with open("./Research.pdf", "wb") as f:
        f.write(pdf_file.getbuffer())
    st.success("PDF file uploaded successfully!")
else:
    st.warning("Please upload a PDF file to start chatting.")

# Setup a session state to store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

@st.cache_resource
def get_vectorstore():
    pdf_name = "./Research.pdf"
    loaders = [PyPDFLoader(pdf_name)]
    # Create chunks of text, aks ChromaDb
    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    ).from_loaders(loaders)
    return index.vectorstore

prompt = st.chat_input(
    "Start typing here..."
)

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    groq_system_prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are a helpful assistant. Your task is to assist the user with their queries. "
        "You will respond with concise and relevant information. "
        "You will not provide any personal opinions or irrelevant information. "
        "Always ensure your responses are clear and to the point."),
        ("human", "{input}")
    ])

    model = "llama3-8b-8192"
    groq_chat = ChatGroq(
        api_key = os.getenv("GROQ_API_KEY"),
        model_name = model,
    )

    try:
        vectorstore = get_vectorstore()

        if vectorstore:

            chain = RetrievalQA.from_chain_type(
                llm=groq_chat,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True
            )

            result = chain({"query": prompt})
            response = result["result"]
            source_docs = result["source_documents"]
            print(response)
            st.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error loading vectorstore: {e}")
        vectorstore = None