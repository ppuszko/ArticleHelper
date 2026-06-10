import { BrowserRouter, Routes, Route, Navigate, useSearchParams } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import ResetPasswordPage from './pages/ResetPasswordPage'
import DashboardPage from './pages/DashboardPage'
import Alert from './components/Alert'

// Shows a one-time banner when redirected with ?registered=1 or ?reset=1
function LoginWithBanner() {
  const [params] = useSearchParams()
  return (
    <div>
      {params.get('registered') && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-sm px-4">
          <Alert type="success">Account created — sign in to continue.</Alert>
        </div>
      )}
      {params.get('reset') && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-sm px-4">
          <Alert type="success">Password updated — sign in with your new password.</Alert>
        </div>
      )}
      <LoginPage />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginWithBanner />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </BrowserRouter>
  )
}
