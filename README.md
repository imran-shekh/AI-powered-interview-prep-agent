# 🤖 AI-Powered Interview Prep Agent

> An AI agent that evaluates real candidate skills using resume + job description, conducts dynamic interviews, identifies gaps, and generates personalized learning plans.

🔗 **Repo:** [imran-shekh/AI-powered-interview-prep-agent](https://github.com/imran-shekh/AI-powered-interview-prep-agent)

---

## 🎯 What It Does

A resume tells you what someone *claims* to know — not how well they *actually* know it.

This agent:
1. Takes a **Job Description** + candidate's **Resume**
2. Extracts and matches skills from both
3. Conducts a **conversational AI interview** on matched skills
4. **Scores** each answer (1–10) with detailed feedback
5. Identifies **skill gaps**
6. Generates a **personalized learning plan** with resources & timelines

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                     │
│   Upload Screen → Interview Screen → Results → Plan      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (Vite Proxy)
┌────────────────────────▼────────────────────────────────┐
│                  BACKEND (FastAPI)                        │
│                                                           │
│  POST /start-interview                                    │
│    ├── PDF Parser (resume text)                          │
│    ├── LLM: Extract resume skills                        │
│    ├── LLM: Extract JD skills                            │
│    ├── Skill Matcher (intersection logic)                │
│    └── InterviewAgent(matched_skills)                    │
│                                                           │
│  POST /answer                                             │
│    ├── LLM: Generate follow-up question                  │
│    └── LLM: Evaluate answer (score + feedback)           │
│                                                           │
│  GET /result                                              │
│    └── Aggregate scores per skill                        │
│                                                           │
│  GET /learning-plan                                       │
│    ├── Weak skills (score < 6)                           │
│    ├── Missing skills (in JD, not in resume)             │
│    └── LLM: Generate plan with resources + timeline      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Groq API (LLaMA 3 / Mixtral)                │
│         Fast inference — free tier used                   │
└─────────────────────────────────────────────────────────┘
```

---

## ⚙️ Scoring Logic

| Score | Meaning |
|-------|---------|
| 8–10  | Strong proficiency |
| 5–7   | Moderate — needs practice |
| 1–4   | Weak — major gap |

- **2 questions per skill** by default
- Average score calculated per skill
- Skills scoring **< 6** are flagged as gaps
- **Missing skills** (present in JD but not resume) are always included in learning plan

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create `.env` file in `backend/`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Start backend:
```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`
API Docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 📁 Project Structure

```
AI Skill Agent/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── agent.py         # Main interview routes
│   │   │   ├── upload.py        # Resume upload
│   │   │   ├── assess.py        # Assessment routes
│   │   │   ├── extract.py       # Skill extraction
│   │   │   └── result.py        # Results
│   │   ├── services/
│   │   │   ├── agent.py         # InterviewAgent class
│   │   │   ├── assessment.py    # Question generation & evaluation
│   │   │   ├── learning_plan.py # Learning plan generation
│   │   │   ├── llm.py           # Groq API wrapper
│   │   │   ├── parser.py        # PDF text extraction
│   │   │   └── scoring.py       # Score aggregation
│   │   ├── utils/
│   │   │   └── prompts.py       # All LLM prompts
│   │   └── main.py              # FastAPI app entry
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx              # All screens
    │   └── App.css              # Styling
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## 🔄 User Flow

```
1. Upload Resume (PDF) + Paste Job Description
        ↓
2. AI extracts skills from both
        ↓
3. Skill matching — finds overlap & gaps
        ↓
4. Conversational interview on matched skills
   (2 questions per skill, scored 1-10)
        ↓
5. Results — score per skill + overall average
        ↓
6. Personalized Learning Plan
   (weak skills + missing skills + resources + timeline)
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Backend | FastAPI + Python |
| LLM | Groq API (LLaMA 3) |
| PDF Parsing | PyPDF2 / pdfplumber |
| Styling | Pure CSS (custom dark theme) |

---

## 🧪 Sample Input / Output

**Input:**
- Resume: Python, Django, SQL, React developer
- JD: Requires Python, FastAPI, Docker, Kubernetes, Redis

**Output:**
```json
{
  "matched_skills": ["Python", "SQL"],
  "missing_skills": ["FastAPI", "Docker", "Kubernetes", "Redis"],
  "final_scores": {
    "Python": 7.5,
    "SQL": 4.0
  },
  "average_score": 5.75
}
```

**Learning Plan includes:**
- SQL deep-dive resources (scored low)
- FastAPI, Docker, Kubernetes, Redis (missing from resume)

---

## 👤 Author

**Imran Shekh**
GitHub: [@imran-shekh](https://github.com/imran-shekh)

---

*Built for Deccan AI Hackathon 2026*
