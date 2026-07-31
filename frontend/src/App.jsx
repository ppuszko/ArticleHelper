import { BrowserRouter, Routes, Route, Navigate, useSearchParams, Link } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import ResetPasswordPage from './pages/ResetPasswordPage'
import DashboardPage from './pages/DashboardPage'
import ProcessDirectoryPage from './pages/ProcessDirectoryPage'
import Alert from './components/Alert'
import CursorGlow from './components/CursorGlow'

function Navbar() {
  return (
    <nav className="fixed top-0 w-full p-4 bg-surface-raised/80 backdrop-blur-md border-b border-surface-border flex justify-between items-center z-50">
      <Link to="/dashboard" className="text-xl font-bold text-text-primary">ArticleAgent</Link>
      <div className="space-x-4">
        <Link to="/process-directory" className="text-text-secondary hover:text-text-primary transition-colors">Ingest</Link>
      </div>
    </nav>
  )
}

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
      <CursorGlow />
      <Navbar />
      <div className="pt-20">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginWithBanner />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/process-directory" element={<ProcessDirectoryPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
