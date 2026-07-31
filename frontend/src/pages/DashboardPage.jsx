import { useNavigate, Link } from 'react-router-dom'
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
        <div className="space-x-4">
            <Link to="/process-directory" className="text-blue-600 hover:underline">Process Directory</Link>
            <button
              onClick={handleLogout}
              className="text-xs text-text-secondary hover:text-status-error transition-colors"
            >
              Sign out
            </button>
        </div>
      </div>
    </div>
  )
}
