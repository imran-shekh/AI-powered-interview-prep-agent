from typing import List
from fastapi import APIRouter, Form, UploadFile, File, Body
from app.services.agent import InterviewAgent, clean_json
from app.services.parser import extract_text_from_pdf
from app.utils.prompts import extract_skills_prompt
from app.services.llm import call_llm
from app.services.learning_plan import generate_learning_plan
from app.services.assessment import detect_ai_answer

router = APIRouter()

_agent = None
_missing_skills = []  # JD mein hai but resume mein nahi


def extract_skills_from_jd(jd_text: str) -> list:
    prompt = f"""
Extract required skills from this Job Description.
Return ONLY JSON: {{"skills": [{{"name": "", "level": "", "type": "technical"}}]}}
JD: {jd_text}
"""
    raw = call_llm(prompt)
    try:
        parsed = clean_json(raw)
        return [s["name"] for s in parsed["skills"]]
    except:
        return []


def match_skills(resume_skills: list, jd_skills: list):
    resume_lower = {s.lower(): s for s in resume_skills}
    jd_lower = {s.lower(): s for s in jd_skills}

    matched = [resume_lower[s] for s in resume_lower if s in jd_lower]
    missing = [jd_lower[s] for s in jd_lower if s not in resume_lower]

    return matched, missing


@router.post("/start-interview")
async def start_interview(
    file: UploadFile = File(...),
    jd_text: str = Form(...)
):
    global _agent, _missing_skills

    # 1. Resume parse
    resume_text = extract_text_from_pdf(file.file)
    resume_prompt = extract_skills_prompt(resume_text)
    resume_raw = call_llm(resume_prompt)

    try:
        resume_json = clean_json(resume_raw)
        resume_skills = [s["name"] for s in resume_json["skills"]]
    except Exception as e:
        return {"error": "Resume skill extraction failed", "detail": str(e)}

    # 2. JD parse
    jd_skills = extract_skills_from_jd(jd_text)
    if not jd_skills:
        return {"error": "JD skill extraction failed"}

    # 3. Match
    matched, missing = match_skills(resume_skills, jd_skills)
    _missing_skills = missing

    # Fallback agar koi match nahi
    if not matched:
        matched = jd_skills[:3]

    # 4. Agent banao sirf matched skills pe
    _agent = InterviewAgent(matched)

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "first_question": _agent.next_question()
    }


@router.post("/answer")
async def answer_question(answer: str = Body(..., embed=True)):
    global _agent
    if _agent is None:
        return {"error": "Interview not started."}
    return _agent.submit_answer(answer.strip())


@router.get("/result")
def get_result():
    global _agent
    if _agent is None:
        return {"error": "Interview not started."}
    return _agent.get_result()


@router.get("/learning-plan")
def get_learning_plan():
    global _agent, _missing_skills
    if _agent is None:
        return {"error": "Interview not started"}

    try:
        result = _agent.get_result()
        weak_skills = [
            skill for skill, score in result["final_scores"].items()
            if score < 6
        ]
        all_gaps = list(set(weak_skills + _missing_skills))

        # Fallback agar koi gap nahi
        if not all_gaps:
            all_gaps = list(result["final_scores"].keys())

        return generate_learning_plan(all_gaps)
    except Exception as e:
        return {"plan": [], "error": str(e)}


@router.post("/answer")
async def answer_question(answer: str = Body(..., embed=True)):
    global _agent
    if _agent is None:
        return {"error": "Interview not started."}


    cheat_check = detect_ai_answer(answer)

    result = _agent.submit_answer(answer.strip())

    # Add cheat check to response
    result["cheat_detection"] = cheat_check

    return result