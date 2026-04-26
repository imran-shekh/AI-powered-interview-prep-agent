from app.services.llm import call_llm
from app.utils.prompts import generate_question_prompt, evaluate_answer_prompt

def generate_question(skill):
    prompt = generate_question_prompt(skill)
    return call_llm(prompt)

def evaluate_answer(skill, question, answer):
    prompt = evaluate_answer_prompt(skill, question, answer)
    return call_llm(prompt)