export default function Alert({ type = 'error', children }) {
  const styles = {
    error: 'border-status-error/30 bg-status-error/10 text-status-error',
    success: 'border-status-success/30 bg-status-success/10 text-status-success',
  }

  return (
    <div className={`rounded-lg border px-4 py-3 text-sm ${styles[type]}`}>
      {children}
    </div>
  )
}
