import { useState } from 'react'
import { Link, useSearchParams, useNavigate } from 'react-router-dom'
import { resetPassword } from '../api/auth'
import AuthLayout from '../components/AuthLayout'
import Field from '../components/Field'
import Alert from '../components/Alert'

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const token = searchParams.get('token') || ''

  const [form, setForm] = useState({ password: '', confirm: '' })
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }))
    setErrors((prev) => ({ ...prev, [e.target.name]: '' }))
    setServerError('')
  }

  function validate() {
    const errs = {}
    if (form.password.length < 8) errs.password = 'Minimum 8 characters.'
    if (form.password !== form.confirm) errs.confirm = 'Passwords do not match.'
    return errs
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length) {
      setErrors(errs)
      return
    }
    setLoading(true)
    setServerError('')
    try {
      await resetPassword({ token, password: form.password })
      navigate('/login?reset=1')
    } catch (err) {
      const detail = err.response?.data?.detail
      setServerError(
        typeof detail === 'string' ? detail : 'The reset link is invalid or has expired.'
      )
    } finally {
      setLoading(false)
    }
  }

  if (!token) {
    return (
      <AuthLayout title="Invalid link" subtitle="This reset link is missing a token.">
        <p className="text-center text-xs text-text-secondary">
          <Link to="/forgot-password" className="text-accent hover:text-accent-hover transition-colors">
            Request a new one
          </Link>
        </p>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout title="Choose new password" subtitle="Pick something you haven't used before">
      <form onSubmit={handleSubmit} className="space-y-4">
        {serverError && <Alert type="error">{serverError}</Alert>}

        <Field label="New password" error={errors.password}>
          <input
            className="auth-input"
            type="password"
            name="password"
            autoComplete="new-password"
            placeholder="Min. 8 characters"
            value={form.password}
            onChange={handleChange}
            required
          />
        </Field>

        <Field label="Confirm new password" error={errors.confirm}>
          <input
            className="auth-input"
            type="password"
            name="confirm"
            autoComplete="new-password"
            placeholder="Repeat password"
            value={form.confirm}
            onChange={handleChange}
            required
          />
        </Field>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Saving…' : 'Set new password'}
        </button>
      </form>
    </AuthLayout>
  )
}
