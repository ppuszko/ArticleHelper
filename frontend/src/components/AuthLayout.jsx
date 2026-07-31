export default function AuthLayout({ title, subtitle, children }) {
  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      {/* subtle grid pattern */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          backgroundImage:
            'linear-gradient(rgba(93,122,81,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(93,122,81,0.05) 1px, transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />

      <div className="w-full max-w-sm relative">
        {/* wordmark */}
        <div className="mb-8 text-center">
          <span className="text-2xl font-semibold tracking-tight text-text-primary">
            app<span className="text-accent">.</span>
          </span>
        </div>

        <div className="auth-card space-y-6">
          <div>
            <h1 className="text-lg font-semibold text-text-primary">{title}</h1>
            {subtitle && (
              <p className="mt-1 text-sm text-text-secondary">{subtitle}</p>
            )}
          </div>
          {children}
        </div>
      </div>
    </div>
  )
}
