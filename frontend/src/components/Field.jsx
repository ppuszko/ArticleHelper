export default function Field({ label, error, children }) {
  return (
    <div className="space-y-1.5">
      {label && <label className="field-label">{label}</label>}
      {children}
      {error && (
        <p className="text-xs text-status-error mt-1">{error}</p>
      )}
    </div>
  )
}
