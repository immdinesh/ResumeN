import { useState } from 'react'
import { analyzePdf, analyzeText, type AnalyzeResult } from './api'
import './App.css'

export default function App() {
  const [mode, setMode] = useState<'pdf' | 'text'>('pdf')
  const [file, setFile] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalyzeResult | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    setFile(f || null)
    setError(null)
    setResult(null)
  }

  const runAnalysis = async () => {
    setError(null)
    setResult(null)
    const job = jobDescription.trim() || 'Software development, programming, technical skills, teamwork, problem solving.'
    setLoading(true)
    try {
      if (mode === 'pdf') {
        if (!file) {
          setError('Please select a PDF resume.')
          return
        }
        const data = await analyzePdf(file, job)
        setResult(data)
      } else {
        if (!resumeText.trim()) {
          setError('Please paste your resume text.')
          return
        }
        const data = await analyzeText(resumeText, job)
        setResult(data)
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Analysis failed. Is the backend running?'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = result
    ? result.similarity_percent >= 50
      ? 'var(--score-high)'
      : result.similarity_percent >= 25
        ? 'var(--score-mid)'
        : 'var(--score-low)'
    : 'var(--text)'

  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">ResumeN</h1>
        <p className="tagline">AI Resume Analyzer — job–resume fit in seconds</p>
      </header>

      <main className="main">
        <div className="tabs">
          <button
            className={mode === 'pdf' ? 'tab active' : 'tab'}
            onClick={() => setMode('pdf')}
          >
            Upload PDF
          </button>
          <button
            className={mode === 'text' ? 'tab active' : 'tab'}
            onClick={() => setMode('text')}
          >
            Paste text
          </button>
        </div>

        <div className="card input-card">
          {mode === 'pdf' ? (
            <div className="upload-zone">
              <input
                type="file"
                accept=".pdf"
                id="pdf-input"
                onChange={handleFileChange}
                className="file-input"
              />
              <label htmlFor="pdf-input" className="upload-label">
                {file ? file.name : 'Choose resume PDF'}
              </label>
            </div>
          ) : (
            <textarea
              className="resume-textarea"
              placeholder="Paste your resume text here…"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              rows={6}
            />
          )}

          <label className="field-label">Job description</label>
          <textarea
            className="job-textarea"
            placeholder="Paste the job description to match against (optional — we’ll use a generic one if empty)."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={4}
          />

          <button
            className="analyze-btn"
            onClick={runAnalysis}
            disabled={loading}
          >
            {loading ? 'Analyzing…' : 'Analyze resume'}
          </button>
        </div>

        {error && (
          <div className="card error-card">
            <span className="error-text">{error}</span>
          </div>
        )}

        {result && (
          <div className="card result-card">
            <h2 className="result-title">Analysis result</h2>
            <div className="score-row">
              <span className="score-label">Job–resume match</span>
              <span className="score-value" style={{ color: scoreColor }}>
                {result.similarity_percent}%
              </span>
            </div>
            <div className="score-bar-wrap">
              <div
                className="score-bar"
                style={{ width: `${result.similarity_percent}%`, backgroundColor: scoreColor }}
              />
            </div>
            <div className="skills-section">
              <h3 className="skills-title">Extracted skills</h3>
              <div className="skills-list">
                {result.skills.length
                  ? result.skills.map((s) => (
                      <span key={s} className="skill-tag">
                        {s}
                      </span>
                    ))
                  : <span className="text-muted">No skills extracted.</span>}
              </div>
            </div>
            {result.resume_preview && (
              <div className="preview-section">
                <h3 className="preview-title">Resume preview</h3>
                <pre className="preview-text">{result.resume_preview}</pre>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <span>ResumeN</span> — TF-IDF · spaCy · FastAPI · React
      </footer>
    </div>
  )
}
