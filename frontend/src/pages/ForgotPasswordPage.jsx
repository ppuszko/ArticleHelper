import { useState } from 'react'
import { Link } from 'react-router-dom'
import { forgotPassword } from '../api/auth'
import AuthLayout from '../components/AuthLayout'
import Field from '../components/Field'
import Alert from '../components/Alert'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await forgotPassword({ email })
      setSent(true)
    } catch (err) {
      // fastapi-users always returns 202 even for unknown emails (security best-practice)
      // so errors here are network/server issues
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Reset password"
      subtitle="Enter your email and we'll send a reset link"
    >
      {sent ? (
        <div className="space-y-4">
          <Alert type="success">
            If that address is registered, a reset link is on its way.
          </Alert>
          <p className="text-center text-xs text-text-secondary">
            <Link to="/login" className="text-accent hover:text-accent-hover transition-colors">
              Back to sign in
            </Link>
          </p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && <Alert type="error">{error}</Alert>}

          <Field label="Email">
            <input
              className="auth-input"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value)
                setError('')
              }}
              required
            />
          </Field>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Sending…' : 'Send reset link'}
          </button>

          <p className="text-center text-xs text-text-secondary">
            <Link to="/login" className="text-accent hover:text-accent-hover transition-colors">
              Back to sign in
            </Link>
          </p>
        </form>
      )}
    </AuthLayout>
  )
}
