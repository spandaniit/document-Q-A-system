from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from .settings import OPENAI_API_KEY

def get_qa_chain(vectordb):
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY),
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
    )
    return qa