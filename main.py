from fastapi import FastAPI

app = FastAPI(title="Smart RAG Chatbot")


@app.get("/")
def root():
    return {"status": "ok"}
