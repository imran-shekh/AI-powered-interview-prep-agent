from app.services.llm import call_llm
from app.utils.prompts import learning_plan_prompt
from app.services.agent import clean_json

def generate_learning_plan(scores):
    global missing_skills_global

    weak_skills = [s for s, v in scores.items() if v < 6]

    # combine missing + weak
    target_skills = list(set(weak_skills + missing_skills_global))

    prompt = f"""
Create a learning plan for:

Skills to improve:
{target_skills}

Include:
- topics
- resources
- time estimate

Return JSON
"""
    return call_llm(prompt)
        