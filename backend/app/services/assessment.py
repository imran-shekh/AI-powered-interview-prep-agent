from app.services.llm import call_llm
from app.utils.prompts import generate_question_prompt, evaluate_answer_prompt

def generate_question(skill):
    prompt = generate_question_prompt(skill)
    return call_llm(prompt)

def evaluate_answer(skill, question, answer):
    prompt = evaluate_answer_prompt(skill, question, answer)
    return call_llm(prompt)

def detect_ai_answer(answer: str) -> dict:
    prompt = f"""
Analyze if this answer was written by a human or AI/copied from internet.

Answer: "{answer}"

Look for:
- Too perfect/formal structure
- No personal thinking or hesitation
- Textbook-like language
- Suspiciously comprehensive for a quick answer

Return ONLY JSON:
{{
  "is_suspicious": true/false,
  "confidence": "high/medium/low",
  "reason": "one line reason"
}}
"""
    raw = call_llm(prompt)
    try:
        from app.services.agent import clean_json
        return clean_json(raw)
    except:
        return {"is_suspicious": False, "confidence": "low", "reason": "Could not analyze"}