import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Trees, Lock, Mail, ArrowRight, AlertCircle } from 'lucide-react'
import { useAuth } from './useAuth'
import Button from '../../components/Button'

export default function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await login({ email, password })
      navigate('/')
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-cream flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-forest text-cream mb-4 shadow-sm">
          <Trees size={24} />
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-ink">
          Sign in to Darukaa.Earth
        </h2>
        <p className="mt-2 text-xs text-ink-muted">
          Access your ecological monitoring projects & satellite telemetry
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 shadow-sm border border-border sm:rounded-xl sm:px-10">
          {error && (
            <div className="mb-4 p-3 rounded-lg bg-amber/10 border border-amber/30 text-amber-dark text-xs flex items-center gap-2">
              <AlertCircle size={16} className="shrink-0 text-amber-dark" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-ink-muted uppercase tracking-wider mb-1.5">
                Email address
              </label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-ink-muted">
                  <Mail size={16} />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@darukaa.earth"
                  className="block w-full pl-9 pr-3 py-2 border border-border rounded-lg text-sm bg-cream focus:outline-none focus:ring-2 focus:ring-forest/30 focus:border-forest text-ink placeholder:text-ink-muted/50"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-ink-muted uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-ink-muted">
                  <Lock size={16} />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="block w-full pl-9 pr-3 py-2 border border-border rounded-lg text-sm bg-cream focus:outline-none focus:ring-2 focus:ring-forest/30 focus:border-forest text-ink placeholder:text-ink-muted/50"
                />
              </div>
            </div>

            <div>
              <Button
                type="submit"
                variant="primary"
                size="md"
                disabled={submitting}
                className="w-full justify-center"
              >
                {submitting ? 'Signing in...' : 'Sign in'}
                {!submitting && <ArrowRight size={15} />}
              </Button>
            </div>
          </form>

          <div className="mt-6 pt-5 border-t border-border text-center">
            <p className="text-xs text-ink-muted">
              Don't have an account?{' '}
              <Link to="/register" className="font-semibold text-forest hover:underline">
                Create an account
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
