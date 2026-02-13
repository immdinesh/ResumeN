const API_BASE = '/api'

export interface AnalyzeResult {
  similarity_score: number
  similarity_percent: number
  skills: string[]
  resume_preview: string
  resume_text?: string
}

export async function analyzeText(
  resumeText: string,
  jobDescription: string
): Promise<AnalyzeResult> {
  const res = await fetch(`${API_BASE}/analyze/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || res.statusText || 'Request failed')
  }
  return res.json()
}

export async function analyzePdf(
  file: File,
  jobDescription: string
): Promise<AnalyzeResult> {
  const form = new FormData()
  form.append('file', file)
  form.append('job_description', jobDescription)
  const res = await fetch(`${API_BASE}/analyze/pdf`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = Array.isArray(err.detail) ? err.detail[0]?.msg : err.detail
    throw new Error(detail || res.statusText || 'Upload failed')
  }
  return res.json()
}
