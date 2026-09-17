import { useState, useMemo, useEffect, useCallback } from 'react'
import { apiFetch } from '../../lib/api'

function normalizeSite(s) {
  return {
    id: s.id,
    name: s.name,
    projectId: s.projectId || s.project_id,
    siteType: s.siteType || s.site_type,
    geometry: s.geometry,
    createdAt: s.createdAt || s.created_at,
  }
}

export function loadSavedSites() {
  return []
}

export function useSites(projects = []) {
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const projectTypeById = useMemo(() => {
    const map = {}
    projects.forEach((p) => {
      if (p.id) map[p.id] = p.type
    })
    return map
  }, [projects])

  const fetchSites = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await apiFetch('/sites')
      const normalized = Array.isArray(data) ? data.map(normalizeSite) : []
      setSites(normalized)
    } catch (err) {
      setError(err.message || 'Failed to load sites')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let isMounted = true
    apiFetch('/sites')
      .then((data) => {
        if (isMounted) {
          setSites(Array.isArray(data) ? data.map(normalizeSite) : [])
          setLoading(false)
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || 'Failed to load sites')
          setLoading(false)
        }
      })
    return () => {
      isMounted = false
    }
  }, [])

  const siteFeatures = useMemo(() => {
    return sites.map((site) => ({
      type: 'Feature',
      geometry: site.geometry,
      properties: {
        id: site.id,
        name: site.name,
        projectId: site.projectId,
        projectType: site.siteType || projectTypeById[site.projectId] || 'carbon',
      },
    }))
  }, [sites, projectTypeById])

  async function addSite({ name, projectId, geometry }) {
    const createdSite = await apiFetch('/sites', {
      method: 'POST',
      body: JSON.stringify({
        name,
        projectId,
        geometry,
      }),
    })
    const normalized = normalizeSite(createdSite)
    setSites((prev) => [normalized, ...prev])
    return normalized
  }

  return { sites, siteFeatures, loading, error, addSite, refreshSites: fetchSites }
}
