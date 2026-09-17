import { useState, useEffect, useCallback } from 'react'
import { apiFetch } from '../../lib/api'

function normalizeProject(p) {
  return {
    id: p.id,
    name: p.name,
    type: p.type,
    status: p.status || 'active',
    description: p.description || '',
    siteCount: p.site_count ?? p.siteCount ?? 0,
    lastUpdated: p.last_updated ?? p.lastUpdated ?? p.created_at ?? new Date().toISOString(),
  }
}

export function loadSavedProjects() {
  // Synchronous initial fallback for components needing instant list initialization
  return []
}

export function useProjects() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchProjects = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await apiFetch('/projects')
      const normalized = Array.isArray(data) ? data.map(normalizeProject) : []
      setProjects(normalized)
    } catch (err) {
      setError(err.message || 'Failed to load projects')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let isMounted = true
    apiFetch('/projects')
      .then((data) => {
        if (isMounted) {
          setProjects(Array.isArray(data) ? data.map(normalizeProject) : [])
          setLoading(false)
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || 'Failed to load projects')
          setLoading(false)
        }
      })
    return () => {
      isMounted = false
    }
  }, [])

  async function addProject({ name, type, description }) {
    const newProj = await apiFetch('/projects', {
      method: 'POST',
      body: JSON.stringify({
        name,
        type,
        status: 'active',
        description: description || '',
      }),
    })
    const normalized = normalizeProject(newProj)
    setProjects((prev) => [normalized, ...prev])
    return normalized
  }

  async function deleteProject(id) {
    await apiFetch(`/projects/${id}`, {
      method: 'DELETE',
    })
    setProjects((prev) => prev.filter((p) => p.id !== id))
  }

  return { projects, loading, error, addProject, deleteProject, refreshProjects: fetchProjects }
}
