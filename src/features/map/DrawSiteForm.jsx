import { useState, useEffect } from 'react'
import Modal from '../../components/Modal'
import Button from '../../components/Button'

const fieldClass =
  'w-full rounded-md border border-border bg-cream px-3 py-2 text-sm text-ink ' +
  'placeholder:text-ink-muted/50 focus:outline-none focus:ring-2 focus:ring-forest/30 focus:border-forest'

export default function DrawSiteForm({ open, projects = [], onClose, onSubmit }) {
  const [name, setName]           = useState('')
  const [projectId, setProjectId] = useState('')

  useEffect(() => {
    if (projects.length > 0 && !projectId) {
      setProjectId(projects[0].id)
    }
  }, [projects, projectId])

  function handleSubmit(e) {
    e.preventDefault()
    const selectedProj = projectId || projects[0]?.id
    if (!name.trim() || !selectedProj) return
    onSubmit({ name: name.trim(), projectId: selectedProj })
    reset()
  }

  function handleClose() {
    reset()
    onClose()
  }

  function reset() {
    setName('')
    setProjectId(projects[0]?.id ?? '')
  }

  return (
    <Modal open={open} onClose={handleClose} title="Name this site">
      <p className="text-xs text-ink-muted mb-4">
        Polygon drawn. Give the site a name and assign it to a project — it'll appear on the map immediately.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-ink-muted uppercase tracking-wide">
            Site name
          </label>
          <input
            type="text"
            required
            autoFocus
            placeholder="e.g. Western Slopes Block A"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={fieldClass}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-ink-muted uppercase tracking-wide">
            Project
          </label>
          <select
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            className={fieldClass}
          >
            {projects.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>

        <div className="flex justify-end gap-2 pt-1">
          <Button type="button" variant="ghost" size="sm" onClick={handleClose}>
            Discard
          </Button>
          <Button type="submit" variant="primary" size="sm" disabled={!name.trim()}>
            Save site
          </Button>
        </div>
      </form>
    </Modal>
  )
}
