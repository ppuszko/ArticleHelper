import { useState } from 'react'
import api from '../api/auth'
import MarkdownRenderer from '../components/MarkdownRenderer'

export default function ProcessDirectoryPage() {
  const [file, setFile] = useState(null)
  const [arxivSignature, setArxivSignature] = useState('')
  const [year, setYear] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingPaper, setLoadingPaper] = useState(false)
  const [error, setError] = useState(null)
  const [processedSections, setProcessedSections] = useState({})
  const [authorInfo, setAuthorInfo] = useState(null)
  const [processedImages, setProcessedImages] = useState({}) // figureLabel -> { figure, filename, description }
  const [texFile, setTexFile] = useState('')

  const handleProcessPaper = async (e, forcedTexFile = null) => {
    e.preventDefault()
    setLoadingPaper(true)
    setError(null)
    setProcessedSections({})
    setAuthorInfo(null)
    setProcessedImages({})

    const targetTexFile = forcedTexFile || texFile
    
    const params = new URLSearchParams({
      tex_file: targetTexFile,
      arxiv_signature: arxivSignature,
      year: year
    })

    const eventSource = new EventSource(`/api/doc/process-paper?${params.toString()}`)
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (event.type === 'message') {
        if (data.event === 'author_info') {
          setAuthorInfo(data.data)
        } else if (data.event === 'processed_section') {
          setProcessedSections(prev => ({ ...prev, [data.id]: { ...data.data, translated: '', summary: '' } }))
        } else if (data.event === 'section_token') {
          setProcessedSections(prev => ({
            ...prev,
            [data.id]: { ...prev[data.id], translated: (prev[data.id]?.translated || '') + data.data.token }
          }))
        } else if (data.event === 'summary_token') {
          setProcessedSections(prev => ({
            ...prev,
            [data.id]: { ...prev[data.id], summary: (prev[data.id]?.summary || '') + data.data.token }
          }))
        } else if (data.event === 'image_start') {
          const key = data.data.figure
          setProcessedImages(prev => ({
            ...prev,
            [key]: { figure: data.data.figure, filename: data.data.filename, description: '' }
          }))
        } else if (data.event === 'image_token') {
          const key = data.data.figure
          setProcessedImages(prev => ({
            ...prev,
            [key]: {
              ...prev[key],
              description: (prev[key]?.description || '') + data.data.token
            }
          }))
        } else if (data.event === 'done') {
          eventSource.close()
          setLoadingPaper(false)
        }
      }
    }
    
    eventSource.onerror = (err) => {
      setError('An error occurred during streaming.')
      eventSource.close()
      setLoadingPaper(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a .gz file first')
      return
    }
    setLoading(true)
    setError(null)
    setResult(null)
    setTexFile('')

    const formData = new FormData()
    formData.append('file', file)
    formData.append('arxiv_signature', arxivSignature)
    formData.append('year', year)

    try {
      const response = await api.post('/doc/process-directory', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(response.data)
      const foundTex = response.data.find(([type, name]) => name.endsWith('.tex'))
      if (foundTex) {
        setTexFile(foundTex[1])
        // Trigger auto-processing if requested by guideline
        setTimeout(() => {
          handleProcessPaper({ preventDefault: () => {} }, foundTex[1])
        }, 100)
      }
    } catch (err) {
      console.error("API Error:", err)
      setError(err.response?.data?.detail || 'An error occurred during processing.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[calc(100vh-5rem)] flex items-center justify-center py-12 px-4 relative z-10">
      <div className="w-full max-w-4xl bg-surface-raised border border-surface-border rounded-3xl p-10 shadow-lg backdrop-blur-md flex flex-col md:flex-row gap-8">
        <div className="flex-1">
          <div className="text-center mb-8">
            <div className="inline-block p-3 bg-accent/10 rounded-full mb-3 text-accent text-2xl">🍃</div>
            <h1 className="text-3xl font-semibold tracking-tight text-text-primary">Data Ingestion</h1>
            <p className="text-sm text-text-secondary mt-2">
              Ingest and unpack LaTeX archives from arXiv for detailed processing
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label className="field-label">Source Archive (.gz)</label>
              <div className="relative border-2 border-dashed border-surface-border hover:border-accent/50 rounded-2xl p-6 transition-all bg-[#fcfbfa]/50 text-center cursor-pointer">
                <input 
                  type="file" 
                  accept=".gz"
                  onChange={(e) => setFile(e.target.files[0])} 
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <div className="space-y-1">
                  <span className="block text-sm text-text-primary font-medium">
                    {file ? file.name : 'Select or drop .gz file'}
                  </span>
                  <span className="block text-xs text-text-secondary">
                    {file ? `${(file.size / 1024).toFixed(1)} KB` : 'Only .gz archive format is accepted'}
                  </span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="field-label">arXiv Signature</label>
                <input 
                  type="text" 
                  placeholder="e.g. 2301.00001" 
                  value={arxivSignature} 
                  onChange={(e) => setArxivSignature(e.target.value)} 
                  className="auth-input" 
                  required 
                />
              </div>
              <div className="space-y-2">
                <label className="field-label">Year</label>
                <input 
                  type="number" 
                  placeholder="e.g. 2023" 
                  value={year} 
                  onChange={(e) => setYear(e.target.value)} 
                  className="auth-input" 
                  required 
                />
              </div>
            </div>

            <button 
              type="submit" 
              disabled={loading} 
              className="btn-primary w-full shadow-sm hover:shadow transition-all font-semibold py-3.5 flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  <span>Processing Archive...</span>
                </>
              ) : (
                <span>Ingest Archive</span>
              )}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 rounded-xl border border-status-error/20 bg-status-error/10 text-status-error text-sm text-center">
              ⚠️ {error}
            </div>
          )}

          {result && (
            <div className="mt-8 p-6 bg-[#fcfbfa] rounded-2xl border border-surface-border shadow-inner">
              <h2 className="font-semibold text-status-success mb-3 flex items-center space-x-2 text-sm uppercase tracking-wider">
                <span>✓</span> <span>Processed Files:</span>
              </h2>
              <div className="max-h-60 overflow-y-auto space-y-2 pr-2">
                {result.map(([type, name], i) => (
                  <div key={i} className="text-xs text-text-secondary bg-surface/40 px-3 py-2 rounded-lg border border-surface-border/40 font-mono break-all flex items-center space-x-2">
                    <span>{type === 'dir' ? '📁' : '📄'}</span>
                    <span>{name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Only show results if texFile exists and we are processing or have processed */}
        {(texFile || Object.keys(processedSections).length > 0 || authorInfo) && (
          <div className="flex-1 w-full max-h-[80vh] overflow-y-auto mt-8 md:mt-0 md:pl-8 md:border-l border-surface-border">
            <h2 className="text-xl font-semibold mb-6">Process Results</h2>
            <form onSubmit={handleProcessPaper} className="mb-6">
              <button type="submit" disabled={loadingPaper || !texFile} className="btn-primary w-full py-2">
                {loadingPaper ? 'Processing...' : 'Run Paper Processor'}
              </button>
            </form>
            <div className="space-y-6">
              {authorInfo && (
                <div className="p-4 bg-surface rounded-lg border border-surface-border">
                  <h3 className="font-bold text-lg mb-1">{authorInfo.title}</h3>
                  <p className="text-sm text-text-secondary">{authorInfo.authors}</p>
                </div>
              )}
              {Object.keys(processedImages).length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-xs font-semibold uppercase tracking-widest text-text-secondary">
                    Image Analysis
                  </h3>
                  {Object.values(processedImages).map((image) => (
                    <div key={image.figure} className="p-5 bg-surface rounded-xl border border-surface-border space-y-3">
                      <div className="flex items-baseline gap-2 border-b border-surface-border pb-2">
                        <span className="font-semibold text-text-primary">{image.figure}</span>
                        <span className="text-xs text-text-secondary font-mono break-all">{image.filename}</span>
                      </div>
                      {image.description ? (
                        <MarkdownRenderer className="text-sm">{image.description}</MarkdownRenderer>
                      ) : (
                        <p className="text-sm text-text-placeholder italic">Analyzing image…</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
              {Object.entries(processedSections).map(([id, section]) => (
                <div key={id} className="p-6 bg-white border border-surface-border rounded-xl shadow-sm space-y-4">
                  <div className="font-bold border-b pb-2 text-lg">{section.section_name}</div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-sm p-3 bg-surface/50 rounded h-48 overflow-y-auto">
                      <MarkdownRenderer className="text-sm">{section.content}</MarkdownRenderer>
                    </div>
                    <div className="text-sm p-3 bg-surface/50 rounded h-48 overflow-y-auto">
                      <MarkdownRenderer className="text-sm">{section.translated}</MarkdownRenderer>
                    </div>
                  </div>
                  <div className="text-sm p-3 bg-surface/50 rounded border-t pt-4 min-h-[4rem]">
                    <MarkdownRenderer className="text-sm">{section.summary}</MarkdownRenderer>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
