from langchain_community.document_loaders import PyPDFLoader
from typing import List
import streamlit as st
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class Helpers:
    def process_pdfs(self, dfs: List[st.runtime.uploaded_file_manager.UploadedFile]) -> List[Document]:
        """Processes the uploaded PDF files and returns text chunks."""
        all_chunks = []
        for pdf in dfs:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf.read())
                tmp_file_path = tmp_file.name

            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)
            all_chunks.extend(chunks)
            print(f"Processed {pdf.name} with {len(chunks)} chunks.")

        return all_chunks
