import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login } from '../api/auth'
import AuthLayout from '../components/AuthLayout'
import Field from '../components/Field'
import Alert from '../components/Alert'

export default function LoginPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }))
    setError('')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const data = await login(form)
      navigate('/dashboard')
    } catch (err) {
      const msg =
        err.response?.data?.detail || 'Invalid email or password.'
      setError(typeof msg === 'string' ? msg : 'Login failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout title="Sign in" subtitle="Welcome back">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <Alert type="error">{error}</Alert>}

        <Field label="Email">
          <input
            className="auth-input"
            type="email"
            name="email"
            autoComplete="email"
            placeholder="you@example.com"
            value={form.email}
            onChange={handleChange}
            required
          />
        </Field>

        <Field label="Password">
          <input
            className="auth-input"
            type="password"
            name="password"
            autoComplete="current-password"
            placeholder="••••••••"
            value={form.password}
            onChange={handleChange}
            required
          />
        </Field>

        <div className="flex justify-end">
          <Link
            to="/forgot-password"
            className="text-xs text-text-secondary hover:text-accent transition-colors"
          >
            Forgot password?
          </Link>
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>

      <p className="text-center text-xs text-text-secondary">
        No account?{' '}
        <Link to="/register" className="text-accent hover:text-accent-hover transition-colors">
          Create one
        </Link>
      </p>
    </AuthLayout>
  )
}
