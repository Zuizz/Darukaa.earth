import { useNavigate } from 'react-router-dom'
import { Trash2 } from 'lucide-react'
import Card from '../../components/Card'

const statusStyles = {
  active:     'bg-forest/10 text-forest',
  monitoring: 'bg-amber/15 text-amber-dark',
  archived:   'bg-ink/8 text-ink-muted',
}

const typeStyles = {
  carbon:       'bg-forest text-cream',
  biodiversity: 'bg-amber text-white',
}

const typeLabels = {
  carbon:       'Carbon',
  biodiversity: 'Biodiversity',
}

// e.g. "2024-11-03" → "3 Nov 2024"
function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export default function ProjectCard({ project, onDelete }) {
  const navigate = useNavigate()
  const { id, name, type, status, siteCount, lastUpdated, description } = project

  return (
    <Card
      className="group flex flex-col gap-3 cursor-pointer hover:shadow-md hover:-translate-y-0.5 transition-all duration-150 relative"
      onClick={() => navigate(`/map?project=${id}`)}
    >
      {/* Header row: type badge + delete button + status pill */}
      <div className="flex items-center justify-between gap-2">
        <span className={`text-[11px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded ${typeStyles[type]}`}>
          {typeLabels[type]}
        </span>
        <div className="flex items-center gap-1.5">
          {onDelete && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation()
                onDelete(project)
              }}
              className="opacity-0 group-hover:opacity-100 p-1 text-ink-muted hover:text-red-600 transition-all rounded"
              title="Delete project"
            >
              <Trash2 size={14} />
            </button>
          )}
          <span className={`text-[11px] font-medium capitalize px-2 py-0.5 rounded-full ${statusStyles[status]}`}>
            {status}
          </span>
        </div>
      </div>

      {/* Name */}
      <h2 className="text-sm font-semibold text-ink leading-snug">{name}</h2>

      {/* Description — clamped to 2 lines */}
      <p className="text-xs text-ink-muted leading-relaxed line-clamp-2">{description}</p>

      {/* Footer: site count + last updated */}
      <div className="flex items-center justify-between mt-auto pt-3 border-t border-border text-xs text-ink-muted">
        <span>{siteCount} {siteCount === 1 ? 'site' : 'sites'}</span>
        <span>Updated {formatDate(lastUpdated)}</span>
      </div>
    </Card>
  )
}
