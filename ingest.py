from .utils import extract_text_from_pdf
from .chunker import chunk_text
from .settings import OPENAI_API_KEY
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def process_file(file_bytes: bytes, filename: str):
    text = ""
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        text = file_bytes.decode("utf-8")

    chunks = chunk_text(text)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma.from_texts(chunks, embeddings)
    return vectordb