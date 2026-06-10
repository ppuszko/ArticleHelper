import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../api/auth'
import AuthLayout from '../components/AuthLayout'
import Field from '../components/Field'
import Alert from '../components/Alert'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', name: '', password: '', confirm: '' })
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
    if (!form.email) errs.email = 'Email is required.'
    if (!form.name) errs.name = 'Name is required'
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
      await register({ email: form.email, password: form.password, name: form.name })
      navigate('/login?registered=1')
    } catch (err) {
      const detail = err.response?.data?.detail
      if (Array.isArray(detail)) {
        setServerError(detail.map((d) => d.msg).join(' '))
      } else {
        setServerError(typeof detail === 'string' ? detail : 'Registration failed.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout title="Create account" subtitle="Get started in seconds">
      <form onSubmit={handleSubmit} className="space-y-4">
        {serverError && <Alert type="error">{serverError}</Alert>}

        <Field label="Email" error={errors.email}>
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

        <Field label="Name" error={errors.name}>
          <input
            className="auth-input"
            type="name"
            name="name"
            autoComplete="name"
            placeholder="Someone"
            value={form.name}
            onChange={handleChange}
            required
          />
        </Field>

        <Field label="Password" error={errors.password}>
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

        <Field label="Confirm password" error={errors.confirm}>
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
          {loading ? 'Creating account…' : 'Create account'}
        </button>
      </form>

      <p className="text-center text-xs text-text-secondary">
        Already have an account?{' '}
        <Link to="/login" className="text-accent hover:text-accent-hover transition-colors">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  )
}
