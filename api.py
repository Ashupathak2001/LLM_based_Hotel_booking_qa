from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from rag_qa import query_rag

app = FastAPI()

#  Define the expected request format
class QueryRequest(BaseModel):
    question: str

#  API Endpoint
@app.post("/ask")
def ask_question(request: QueryRequest):
    answer = query_rag(request.question)
    return {"question": request.question, "answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

