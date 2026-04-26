import json
from fastapi import APIRouter
from app.services.llm import call_llm
from app.utils.prompts import extract_skills_prompt

router = APIRouter()

def clean_json(raw: str) -> dict:
    start = raw.find('{')
    end = raw.rfind('}')
    
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in response")
    
    json_str = raw[start:end+1]
    return json.loads(json_str)

@router.post("/extract-skills")
def extract_skills(text: str):
    prompt = extract_skills_prompt(text)
    result = call_llm(prompt)

    try:
        parsed = clean_json(result)  # ✅ clean_json_response → clean_json
        return parsed
    except Exception as e:
        return {
            "error": "Failed to parse JSON",
            "raw_output": result
        }