/**
 * PageHeader — shared top-of-page heading block.
 *
 * Props:
 *   title (string)       — main heading
 *   subtitle (string?)   — optional descriptive line beneath
 *   actions (ReactNode?) — slot for right-aligned buttons / controls
 */
export default function PageHeader({ title, subtitle, actions }) {
  return (
    <header className="flex items-start justify-between px-8 pt-8 pb-6 border-b border-border">
      <div>
        <h1 className="text-2xl font-semibold text-ink tracking-tight">{title}</h1>
        {subtitle && (
          <p className="mt-1 text-sm text-ink-muted">{subtitle}</p>
        )}
      </div>
      {actions && <div className="flex items-center gap-3">{actions}</div>}
    </header>
  )
}
