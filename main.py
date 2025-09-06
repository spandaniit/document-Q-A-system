from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from rag.ingest import process_file
from rag.retriever import get_qa_chain

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = None
qa_chain = None

@app.post("/upload")
async def upload_file(file: UploadFile):
    global db, qa_chain
    db = process_file(await file.read(), file.filename)
    qa_chain = get_qa_chain(db)
    return {"status": "success", "message": "File processed successfully"}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    global qa_chain
    if not qa_chain:
        return {"error": "No document uploaded yet."}
    result = qa_chain({"query": query})
    return {
        "answer": result["result"],
        "sources": [doc.page_content[:300] for doc in result["source_documents"]],
    }