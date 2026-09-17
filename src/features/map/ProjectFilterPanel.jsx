import { SITE_COLORS } from '../../lib/siteColors'

export default function ProjectFilterPanel({ sites = [], projects = [], activeProjectIds = new Set(), onToggle, onSelectAll, onClearAll }) {
  // Count live sites (includes drawn ones) per project
  const siteCountByProject = sites.reduce((acc, site) => {
    const pId = String(site.projectId || site.project_id || '')
    if (pId) {
      acc[pId] = (acc[pId] ?? 0) + 1
    }
    return acc
  }, {})

  return (
    <aside className="w-60 shrink-0 bg-white border-r border-border flex flex-col overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <h2 className="text-[11px] font-semibold uppercase tracking-wider text-ink-muted">
          Projects
        </h2>
        <div className="flex gap-3">
          <button onClick={onSelectAll} className="text-xs text-forest hover:underline">All</button>
          <button onClick={onClearAll}  className="text-xs text-ink-muted hover:underline">None</button>
        </div>
      </div>

      <ul className="overflow-y-auto flex-1 py-1">
        {projects.map((project) => {
          const pStrId  = String(project.id)
          const count   = siteCountByProject[pStrId] ?? 0
          const isActive = activeProjectIds.has(project.id) || activeProjectIds.has(pStrId)
          const color   = SITE_COLORS[project.type]?.fill ?? '#888'

          return (
            <li key={project.id}>
              <button
                onClick={() => onToggle(project.id)}
                className={`w-full flex items-start gap-3 px-4 py-2.5 text-left transition-colors hover:bg-cream ${
                  isActive ? '' : 'opacity-40'
                }`}
              >
                {/* Type color dot */}
                <span
                  className="mt-0.5 w-2.5 h-2.5 rounded-full shrink-0 ring-1 ring-black/10"
                  style={{ backgroundColor: color }}
                />

                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-ink leading-snug truncate">
                    {project.name}
                  </p>
                  <p className="text-[11px] text-ink-muted mt-0.5">
                    {count} {count === 1 ? 'site' : 'sites'} · {project.type}
                  </p>
                </div>

                {/* Checkbox */}
                <span
                  className={`mt-0.5 w-3.5 h-3.5 rounded border shrink-0 flex items-center justify-center transition-colors ${
                    isActive ? 'bg-forest border-forest' : 'border-border'
                  }`}
                >
                  {isActive && (
                    <svg viewBox="0 0 10 8" className="w-2 h-1.5" fill="none">
                      <path d="M1 4l3 3 5-6" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </span>
              </button>
            </li>
          )
        })}
      </ul>

      <div className="px-4 py-3 border-t border-border">
        <p className="text-[11px] text-ink-muted">
          Click the polygon tool to draw a new site.
        </p>
      </div>
    </aside>
  )
}
