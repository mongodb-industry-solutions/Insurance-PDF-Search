from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from ask_llm import interrogate_llm

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.post("/askTheLlm")
async def ask_llm(request: Request):
    data = await request.json()
    question = data.get("question")
    llm_output = interrogate_llm(question)
    return {"question": question, "result": llm_output}
