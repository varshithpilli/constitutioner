from fastapi import FastAPI, Request
from pydantic import BaseModel
from deploy_model import Constitutioner
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://constitutioner.varzone.in"],
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    answer_generator = engine.inference(query)
    
    def iter_response():
        try:
            for chunk in answer_generator:
                yield chunk.encode("utf-8")
        except Exception:
            yield b"\n[Error occurred while streaming response]"

    return StreamingResponse(iter_response(), media_type="text/plain")
    
    # return answer_generator
