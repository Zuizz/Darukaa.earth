import { useRef, useState, useEffect, useMemo } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Globe, Layers } from 'lucide-react'
import 'mapbox-gl/dist/mapbox-gl.css'
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css'

import PageHeader from '../../components/PageHeader'
import ProjectFilterPanel from './ProjectFilterPanel'
import DrawSiteForm from './DrawSiteForm'
import { useSites } from './useSites'
import { useMapSetup } from './useMapSetup'
import { useMapDraw } from './useMapDraw'
import { useProjects } from '../projects/useProjects'

export default function MapView() {
  const navigate      = useNavigate()
  const [searchParams] = useSearchParams()
  const targetProjectId = searchParams.get('project')
  const containerRef  = useRef(null)

  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/satellite-v9')

  const { projects } = useProjects()
  const { sites, siteFeatures, addSite } = useSites(projects)

  const allProjectIds = useMemo(() => new Set(projects.map((p) => p.id)), [projects])
  const [activeProjectIds, setActiveProjectIds] = useState(() => {
    return targetProjectId ? new Set([targetProjectId]) : new Set()
  })

  // Keep activeProjectIds in sync when projects load or URL query param changes
  useEffect(() => {
    if (targetProjectId) {
      setActiveProjectIds(new Set([targetProjectId]))
    } else if (projects.length > 0) {
      setActiveProjectIds(new Set(projects.map((p) => p.id)))
    }
  }, [projects, targetProjectId])

  const map = useMapSetup(
    containerRef,
    siteFeatures,
    activeProjectIds,
    (siteId) => navigate(`/site/${siteId}`),
    mapStyle,
  )

  const { pendingFeature, handleDrawComplete, handleDrawCancel } = useMapDraw(map)

  function toggleProject(projectId) {
    setActiveProjectIds((prev) => {
      const next = new Set(prev)
      if (next.has(projectId)) {
        next.delete(projectId)
      } else {
        next.add(projectId)
      }
      return next
    })
  }

  async function handleSiteSubmit({ name, projectId }) {
    if (!pendingFeature) return
    await addSite({ name, projectId, geometry: pendingFeature.geometry })
    handleDrawComplete()
  }

  const noToken = !import.meta.env.VITE_MAPBOX_TOKEN

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader
        title="Map"
        subtitle="Geospatial view of all project sites."
      />

      {noToken && (
        <div className="px-6 py-2.5 bg-amber/10 border-b border-amber/30 text-xs text-amber-dark">
          <code className="font-mono">VITE_MAPBOX_TOKEN</code> is not set.
          Copy <code className="font-mono">.env.example</code> to <code className="font-mono">.env</code>, fill in your token, and restart the dev server.
        </div>
      )}

      <div className="flex flex-1 overflow-hidden">
        <ProjectFilterPanel
          sites={sites}
          projects={projects}
          activeProjectIds={activeProjectIds}
          onToggle={toggleProject}
          onSelectAll={() => setActiveProjectIds(new Set(allProjectIds))}
          onClearAll={() => setActiveProjectIds(new Set())}
        />

        <div ref={containerRef} className="flex-1 min-h-0 w-full h-full relative">
          {/* Basemap Style Switcher Floating Pill */}
          <div className="absolute top-4 right-4 z-10 bg-white/90 backdrop-blur-md border border-border shadow-md rounded-lg p-1 flex items-center gap-1">
            <button
              type="button"
              onClick={() => setMapStyle('mapbox://styles/mapbox/satellite-v9')}
              className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium transition-all ${
                mapStyle === 'mapbox://styles/mapbox/satellite-v9'
                  ? 'bg-forest text-cream shadow-sm'
                  : 'text-ink-muted hover:text-ink hover:bg-cream'
              }`}
            >
              <Globe size={13} />
              Satellite
            </button>
            <button
              type="button"
              onClick={() => setMapStyle('mapbox://styles/mapbox/satellite-streets-v12')}
              className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium transition-all ${
                mapStyle === 'mapbox://styles/mapbox/satellite-streets-v12'
                  ? 'bg-forest text-cream shadow-sm'
                  : 'text-ink-muted hover:text-ink hover:bg-cream'
              }`}
            >
              <Layers size={13} />
              Satellite + Streets
            </button>
          </div>
        </div>
      </div>

      <DrawSiteForm
        open={!!pendingFeature}
        projects={projects}
        onClose={handleDrawCancel}
        onSubmit={handleSiteSubmit}
      />
    </div>
  )
}
