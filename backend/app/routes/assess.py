from fastapi import APIRouter
from app.services.assessment import generate_question, evaluate_answer

router = APIRouter()

@router.post("/question")
def get_question(skill: str):
    return {"question": generate_question(skill)}

@router.post("/evaluate")
def evaluate(skill: str, question: str, answer: str):
    return evaluate_answer(skill, question, answer)