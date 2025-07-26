from fastapi import FastAPI, Request
from pydantic import BaseModel
from .deploy_model import Constitutioner

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

engine = Constitutioner()

@app.get("/")
def landing():
    return {"message": "Landed successfully"}

@app.post("/ask")
async def ask_constitution(req: QueryRequest):
    query = req.question.strip()
    if not query:
        return {"answer": "Please provide a valid question."}
    answer = engine.inference(query)
    if answer is None:
        return {"answer": "Sorry, the Constitution does not contain relevant information about this query."}
    return {"answer": answer}
