from fastapi import FastAPI, Request
from routes.route import router
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

@app.get("/testAskLlm")
async def test_ask_llm():
    hardcoded_question = "To calculate repair time use claimFNOLdate as start date and claimCloseDate as end date."
    llm_output = interrogate_llm(hardcoded_question)
    return {"question": hardcoded_question, "result": llm_output}

# @router.get("/{question}")
#async def aksTheLlm(question: str):
#    llm_output = interrogate_llm(question)
#    return {"result": llm_output} 

@app.post("/testTheLlm")
async def test_ask_llm(request: Request):
    data = await request.json()
    question = data.get("question")
    llm_output = interrogate_llm(question)
    return {"question": question, "result": llm_output}

#app.include_router(router)