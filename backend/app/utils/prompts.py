def extract_skills_prompt(text):
    return f"""
Extract skills from this resume or JD.

Return JSON:
{{
  "skills": [
    {{"name": "", "level": "", "type": "technical"}}
  ]
}}

Text:
{text}
"""


def generate_question_prompt(skill):
    return f"""
Generate a technical interview question for {skill}.

If skill is strong → ask medium/hard question
Focus on practical understanding.

Return ONLY question.
"""


def evaluate_answer_prompt(skill, question, answer):
    return f"""
You are a STRICT technical interviewer.

Skill: {skill}

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer VERY STRICTLY.

Rules:
- If answer is wrong → score MUST be between 0-3
- If partially correct → 4-6
- If mostly correct → 7-8
- If perfect → 9-10
- DO NOT give high score for incorrect answers
- DO NOT be lenient
- Penalize vague or incomplete answers

Also check:
- Technical correctness
- Completeness
- Code quality (if code is provided)

Return ONLY valid JSON:
{{
  "score": number,
  "feedback": "short and strict feedback"
}}
"""

def learning_plan_prompt(gaps):
    return f"""
Create a personalized learning plan based on skill gaps.

Gaps:
{gaps}

Return JSON:
{{
  "plan": [
    {{
      "skill": "",
      "topics": [],
      "resources": [],
      "timeline": ""
    }}
  ]
}}
"""