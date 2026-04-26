import { useState, useRef } from 'react'
import './App.css'

const API = '/api'
const STEPS = ['Upload', 'Interview', 'Results', 'Learning Plan']

function scoreColor(score) {
  if (score >= 7) return '#00d9a3'
  if (score >= 4) return '#ffd166'
  return '#ff4d6d'
}

// ─── UPLOAD SCREEN ───────────────────────────────────────────
function UploadScreen({ onStart }) {
  const [file, setFile] = useState(null)
  const [jd, setJd] = useState('')
  const [drag, setDrag] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const fileRef = useRef()

  const handleDrop = (e) => {
    e.preventDefault(); setDrag(false)
    const f = e.dataTransfer.files[0]
    if (f?.type === 'application/pdf') setFile(f)
  }

  const handleUpload = async () => {
    if (!file || !jd.trim()) { setError('Please upload resume and enter job description'); return }
    setLoading(true); setError('')
    try {
      const form = new FormData()
      form.append('file', file)
      form.append('jd_text', jd)
      const res = await fetch(`${API}/start-interview`, { method: 'POST', body: form })
      const data = await res.json()
      if (data.error) { setError(data.error); return }
      onStart(data)
    } catch {
      setError('Server error. Is backend running on port 8000?')
    } finally { setLoading(false) }
  }

  return (
    <div className="container">
      <div className="hero-tag">✦ AI-Powered Assessment</div>
      <h1>Know your <span>real skills</span>, not just what's on paper.</h1>
      <p className="subtitle">
        Upload your resume and paste a job description. Our AI will assess your
        real proficiency and generate a personalized learning plan.
      </p>

      <div
        className={`upload-zone ${drag ? 'drag' : ''}`}
        onClick={() => fileRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDrag(true) }}
        onDragLeave={() => setDrag(false)}
        onDrop={handleDrop}
      >
        <input ref={fileRef} type="file" accept=".pdf" hidden onChange={(e) => setFile(e.target.files[0])} />
        <div className="upload-icon">{file ? '📄' : '☁️'}</div>
        <strong style={{ fontFamily: 'Syne', fontSize: '1rem' }}>
          {file ? 'Resume ready!' : 'Drop your resume here'}
        </strong>
        <p>{file ? '' : 'or click to browse — PDF only'}</p>
        {file && <div className="file-name">✓ {file.name}</div>}
      </div>

      <textarea
        className="jd-input"
        placeholder="Paste Job Description here..."
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />

      {error && <div className="error-msg">{error}</div>}

      <button className="btn btn-primary" onClick={handleUpload} disabled={!file || !jd || loading}>
        {loading ? '⏳ Starting interview...' : '→ Start JD-Based Assessment'}
      </button>
    </div>
  )
}

// ─── INTERVIEW SCREEN ─────────────────────────────────────────
function InterviewScreen({ initialData, onFinish }) {
  const [currentSkill, setCurrentSkill] = useState(initialData.first_question?.skill || '')
  const [question, setQuestion] = useState(initialData.first_question?.question || '')
  const [evaluation, setEvaluation] = useState(null)
  const [done, setDone] = useState(initialData.first_question?.done || false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const answerRef = useRef('')

  const handleAnswer = async () => {
    const ans = answerRef.current
    if (!ans.trim()) return
    setLoading(true); setError(''); setEvaluation(null)
    try {
      const res = await fetch(`${API}/answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer: ans })
      })
      const data = await res.json()
      if (data.error) { setError(data.error); return }
      setEvaluation(data.evaluation)
      answerRef.current = ''
      const ta = document.getElementById('answer-box')
      if (ta) ta.value = ''
      if (data.next?.done) {
        setDone(true)
      } else {
        setCurrentSkill(data.next?.skill || '')
        setQuestion(data.next?.question || '')
      }
    } catch {
      setError('Server error.')
    } finally { setLoading(false) }
  }

  return (
    <div className="container">
      <div className="steps">
        {STEPS.map((s, i) => (
          <div key={s} className={`step-dot ${i === 1 ? 'active' : i < 1 ? 'done' : ''}`} title={s} />
        ))}
        <span style={{ marginLeft: '0.5rem', fontSize: '0.7rem', color: 'var(--muted)' }}>Interview in progress</span>
      </div>

      {done ? (
        <>
          <div className="done-banner">🎉 Interview Complete!</div>
          <p style={{ color: 'var(--muted)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            All skills assessed. Ready to see your results?
          </p>
          {error && <div className="error-msg">{error}</div>}
          <button className="btn btn-primary" onClick={onFinish} disabled={loading}>
            {loading ? '⏳ Calculating...' : '→ View Results'}
          </button>
        </>
      ) : (
        <>
          <div className="skill-badge">◆ Skill: {currentSkill}</div>

          {evaluation && (
            <div className="eval-card">
              <div>
                <div className="eval-label">Last Score</div>
                <div className={`eval-score ${evaluation.score >= 7 ? 'high' : evaluation.score >= 4 ? 'mid' : 'low'}`}>
                  {evaluation.score}<span style={{ fontSize: '0.9rem', fontFamily: 'DM Mono' }}>/10</span>
                </div>
              </div>
              <div>
                <div className="eval-label">Feedback</div>
                <div className="eval-feedback">{evaluation.feedback}</div>
              </div>
            </div>
          )}

          <div className="question-card">
            <div className="q-label">Question</div>
            <div className="question-text">{question}</div>
          </div>

          <textarea
            id="answer-box"
            placeholder="Type your answer here..."
            onChange={(e) => { answerRef.current = e.target.value }}
            onKeyDown={(e) => { if (e.key === 'Enter' && e.ctrlKey) handleAnswer() }}
          />
          <div style={{ fontSize: '0.65rem', color: 'var(--muted)', marginTop: '0.4rem' }}>Ctrl+Enter to submit</div>

          {error && <div className="error-msg">{error}</div>}

          <button className="btn btn-primary" onClick={handleAnswer} disabled={loading}>
            {loading ? '⏳ Evaluating...' : '→ Submit Answer'}
          </button>
        </>
      )}
    </div>
  )
}

// ─── RESULT SCREEN ────────────────────────────────────────────
function ResultScreen({ scores, avgScore, onPlan }) {
  const [loading, setLoading] = useState(false)
  const handlePlan = async () => { setLoading(true); await onPlan(); setLoading(false) }

  return (
    <div className="container">
      <div className="section-title">Your Assessment Results</div>
      <div className="avg-score-display">{avgScore}<span style={{ fontSize: '2rem' }}>/10</span></div>
      <p style={{ textAlign: 'center', color: 'var(--muted)', fontSize: '0.8rem', marginBottom: '2rem' }}>Overall Average Score</p>

      <div className="result-grid">
        {Object.entries(scores).map(([skill, score], i) => (
          <div className="skill-row" key={skill} style={{ animationDelay: `${i * 0.05}s` }}>
            <div className="skill-name">{skill}</div>
            <div className="score-bar-wrap">
              <div className="score-bar" style={{ width: `${score * 10}%`, background: scoreColor(score) }} />
            </div>
            <div className="skill-score" style={{ color: scoreColor(score) }}>{score}</div>
          </div>
        ))}
      </div>

      <button className="btn btn-primary" onClick={handlePlan} disabled={loading}>
        {loading ? '⏳ Generating plan...' : '→ Get Learning Plan'}
      </button>
    </div>
  )
}

// ─── PLAN SCREEN ──────────────────────────────────────────────
function PlanScreen({ plan, onReset }) {
  return (
    <div className="container">
      <div className="hero-tag">✦ Personalized for you</div>
      <div className="section-title">Your Learning Plan</div>

      {plan.length === 0 && (
        <p style={{ color: 'var(--muted)', fontSize: '0.85rem' }}>
          Great news — no major skill gaps found!
        </p>
      )}

      {plan.map((item, i) => (
        <div className="plan-card" key={i} style={{ animationDelay: `${i * 0.08}s` }}>
          <div className="plan-skill">
            <span>◆ {item.skill}</span>
            {item.timeline && <span className="plan-timeline">{item.timeline}</span>}
          </div>
          {item.topics?.length > 0 && (
            <div className="plan-topics">
              {item.topics.map((t, j) => <span className="topic-tag" key={j}>{t}</span>)}
            </div>
          )}
          {item.resources?.length > 0 && (
            <ul className="plan-resources">
              {item.resources.map((r, j) => <li key={j}>{r}</li>)}
            </ul>
          )}
        </div>
      ))}

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onReset}>↺ New Assessment</button>
        <button className="btn btn-primary" onClick={() => window.print()}>↓ Save Plan</button>
      </div>
    </div>
  )
}

// ─── MAIN APP ─────────────────────────────────────────────────
export default function App() {
  const [step, setStep] = useState(0)
  const [uploadData, setUploadData] = useState(null)
  const [scores, setScores] = useState({})
  const [avgScore, setAvgScore] = useState(0)
  const [plan, setPlan] = useState([])

  const handleStart = (data) => { setUploadData(data); setStep(1) }

  const handleFinish = async () => {
    const res = await fetch(`${API}/result`)
    const data = await res.json()
    setScores(data.final_scores || {})
    setAvgScore(data.average_score || 0)
    setStep(2)
  }

  const handlePlan = async () => {
    const res = await fetch(`${API}/learning-plan`)
    const data = await res.json()
    setPlan(data.plan || [])
    setStep(3)
  }

  const reset = () => { setStep(0); setUploadData(null); setScores({}); setAvgScore(0); setPlan([]) }

  return (
    <div className="app">
      <nav>
        <div className="logo">SkillAgent.AI</div>
        <div className="nav-step">{STEPS[step]}</div>
      </nav>
      <main>
        {step === 0 && <UploadScreen onStart={handleStart} />}
        {step === 1 && <InterviewScreen initialData={uploadData} onFinish={handleFinish} />}
        {step === 2 && <ResultScreen scores={scores} avgScore={avgScore} onPlan={handlePlan} />}
        {step === 3 && <PlanScreen plan={plan} onReset={reset} />}
      </main>
    </div>
  )
}
