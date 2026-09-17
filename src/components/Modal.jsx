import { useEffect } from 'react'
import { X } from 'lucide-react'

/**
 * Modal — portal-free dialog built on the native <dialog> element.
 *
 * Props:
 *   open     (bool)   — controlled open state
 *   onClose  (fn)     — called when the user dismisses
 *   title    (string)
 *   children (node)
 *   width    (string, default 'max-w-lg') — Tailwind max-width class
 */
export default function Modal({ open, onClose, title, children, width = 'max-w-lg' }) {
  // Close on Escape key
  useEffect(() => {
    if (!open) return
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [open, onClose])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-ink/40"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Panel */}
      <div className={`relative bg-white rounded-xl shadow-lg ${width} w-full mx-4`}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-border">
          <h2 className="text-base font-semibold text-ink">{title}</h2>
          <button
            onClick={onClose}
            className="text-ink-muted hover:text-ink transition-colors"
            aria-label="Close"
          >
            <X size={18} />
          </button>
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>
  )
}
