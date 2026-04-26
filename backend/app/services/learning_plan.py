from app.services.llm import call_llm
from app.utils.prompts import learning_plan_prompt
from app.services.agent import clean_json

def generate_learning_plan(gaps):
    if not gaps:
        return {"plan": []}
    
    try:
        prompt = learning_plan_prompt(gaps)
        raw = call_llm(prompt)
        return clean_json(raw)
    except Exception as e:
        # Fallback plan agar LLM fail ho
        return {
            "plan": [
                {
                    "skill": skill,
                    "topics": ["Fundamentals", "Practice projects"],
                    "resources": ["Official documentation", "YouTube tutorials"],
                    "timeline": "2-4 weeks"
                }
                for skill in gaps
            ]
        }