from fastapi import APIRouter
from ask_llm import interrogate_llm

router = APIRouter()

@router.get("/{question}")
async def askLlm(question: str):
    llm_output = interrogate_llm(question)
    return {"result": llm_output}