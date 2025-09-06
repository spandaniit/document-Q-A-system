import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# ---------------------------
# Streamlit App Config
# ---------------------------
st.set_page_config(page_title="📘 RAG Q&A System", layout="wide")

st.title("📘 Retrieval-Augmented Generation (RAG) Q&A System")
st.markdown("Upload a PDF, ask questions in natural language, and get contextual answers with references.")

# ---------------------------
# File Uploader
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your PDF file", type=["pdf"])

if uploaded_file:
    # Extract text
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        st.error("❌ Could not extract text from this PDF. Try another file.")
    else:
        # ---------------------------
        # Chunking
        # ---------------------------
        st.info("🔄 Processing document...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_text(text)

        # ---------------------------
        # Embeddings + Vector DB
        # ---------------------------
        embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])
        vectordb = Chroma.from_texts(chunks, embeddings)

        # ---------------------------
        # RetrievalQA
        # ---------------------------
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"]),
            retriever=vectordb.as_retriever(),
            return_source_documents=True
        )

        # ---------------------------
        # User Query
        # ---------------------------
        query = st.text_input("💬 Ask a question about the document:")

        if query:
            with st.spinner("🤔 Thinking..."):
                result = qa_chain({"query": query})

            # ---------------------------
            # Show Answer
            # ---------------------------
            st.subheader("✅ Answer")
            st.write(result["result"])

            # ---------------------------
            # Show Sources
            # ---------------------------
            with st.expander("📖 Sources / References"):
                for i, doc in enumerate(result["source_documents"]):
                    st.markdown(f"**Source {i+1}:** {doc.page_content[:500]}...")