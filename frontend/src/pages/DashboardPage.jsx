import { useNavigate } from 'react-router-dom'
import { logout } from '../api/auth'

export default function DashboardPage() {
  const navigate = useNavigate()

  async function handleLogout() {
    try {
      await logout()
    } catch {
      // ignore — still clear local token
    }
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="text-center space-y-4">
        <h1 className="text-2xl font-semibold text-text-primary">You're in.</h1>
        <p className="text-text-secondary text-sm">
          Replace this page with your application.
        </p>
        <button
          onClick={handleLogout}
          className="mt-4 text-xs text-text-secondary hover:text-status-error transition-colors"
        >
          Sign out
        </button>
      </div>
    </div>
  )
}
