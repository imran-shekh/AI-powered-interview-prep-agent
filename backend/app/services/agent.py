from app.services.assessment import generate_question, evaluate_answer
import json

def clean_json(raw: str) -> dict:
    start = raw.find('{')
    end = raw.rfind('}')
    if start == -1 or end == -1:
        raise ValueError("No JSON found")
    return json.loads(raw[start:end+1])


class InterviewAgent:
    def __init__(self, skills):
        self.skills = skills
        self.current_skill_index = 0
        self.questions_asked = 0
        self.max_questions_per_skill = 2
        self.scores = {skill: [] for skill in skills}
        self.current_question = None

    def next_question(self):
        if self.current_skill_index >= len(self.skills):
            return {"message": "Interview complete", "done": True}

        skill = self.skills[self.current_skill_index]
        question = generate_question(skill)
        self.current_question = question
        self.questions_asked += 1

        return {
            "skill": skill,
            "question": question,
            "done": False
        }

    def submit_answer(self, answer):
        if self.current_skill_index >= len(self.skills):
            return {"message": "Interview already complete", "done": True}

        skill = self.skills[self.current_skill_index]

        try:
            evaluation_raw = evaluate_answer(skill, self.current_question, answer)
            evaluation = clean_json(evaluation_raw)

            score = evaluation.get("score", 0)
            feedback = evaluation.get("feedback", "No feedback")

            # 🔥 HARD RULES (force strictness)
            if len(answer.strip()) < 15:
                score = min(score, 2)

            if "class" not in answer and "def" not in answer and len(answer) > 30:
                score = min(score, 5)

        except Exception as e:
            score = 0
            feedback = f"Evaluation failed: {str(e)}"

        self.scores[skill].append(score)

        if self.questions_asked >= self.max_questions_per_skill:
            self.current_skill_index += 1
            self.questions_asked = 0

        next_q = self.next_question()

        return {
            "evaluation": {
                "score": score,
                "feedback": feedback
            },
            "next": next_q
        }

    def get_result(self):
        final_scores = {}
        for skill, scores in self.scores.items():
            avg = round(sum(scores) / len(scores), 2) if scores else 0
            final_scores[skill] = avg

        return {
            "final_scores": final_scores,
            "total_skills": len(self.skills),
            "average_score": round(
                sum(final_scores.values()) / len(final_scores), 2
            ) if final_scores else 0
        }