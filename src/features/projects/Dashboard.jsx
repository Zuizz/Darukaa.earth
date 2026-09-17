import { useState } from "react";
import { Plus, Loader2, AlertTriangle } from "lucide-react";
import PageHeader from "../../components/PageHeader";
import Button from "../../components/Button";
import Modal from "../../components/Modal";
import ProjectCard from "./ProjectCard";
import NewProjectModal from "./NewProjectModal";
import CanopySVG from "./CanopySVG";
import { useProjects } from "./useProjects";

const FILTER_OPTIONS = [
  { value: "all", label: "All" },
  { value: "carbon", label: "Carbon" },
  { value: "biodiversity", label: "Biodiversity" },
];

function FilterTabs({ active, onChange }) {
  return (
    <div className="flex gap-1 bg-cream-dark rounded-lg p-1">
      {FILTER_OPTIONS.map(({ value, label }) => (
        <button
          key={value}
          onClick={() => onChange(value)}
          className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
            active === value
              ? "bg-white text-ink shadow-sm"
              : "text-ink-muted hover:text-ink"
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

export default function Dashboard() {
  const { projects, loading, addProject, deleteProject } = useProjects();
  const [filter, setFilter] = useState("all");
  const [modalOpen, setModalOpen] = useState(false);
  const [deletingProject, setDeletingProject] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const visible =
    filter === "all" ? projects : projects.filter((p) => p.type === filter);

  async function handleConfirmDelete() {
    if (!deletingProject) return;
    setIsDeleting(true);
    try {
      await deleteProject(deletingProject.id);
      setDeletingProject(null);
    } catch {
      /* ignore / handled by apiFetch error */
    } finally {
      setIsDeleting(false);
    }
  }

  return (
    <div className="flex flex-col h-full overflow-y-auto">
      <PageHeader
        title="Projects"
        subtitle={`${projects.length} project${projects.length !== 1 ? "s" : ""} across carbon and biodiversity programmes.`}
        actions={
          <Button
            variant="primary"
            size="sm"
            onClick={() => setModalOpen(true)}
          >
            <Plus size={14} strokeWidth={2.5} />
            New project
          </Button>
        }
      />

      {/* Toolbar */}
      <div className="flex items-center gap-4 px-8 py-4 border-b border-border">
        <FilterTabs active={filter} onChange={setFilter} />
        <span className="ml-auto text-xs text-ink-muted">
          {visible.length} shown
        </span>
      </div>

      {/* Grid or empty state */}
      <div className="flex-1 px-8 py-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3 text-ink-muted">
            <Loader2 size={24} className="animate-spin text-forest" />
            <p className="text-xs">Fetching projects from API...</p>
          </div>
        ) : visible.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {visible.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onDelete={setDeletingProject}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            isFiltered={filter !== "all"}
            onAdd={() => setModalOpen(true)}
          />
        )}
      </div>

      <NewProjectModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={addProject}
      />

      {/* Delete Confirmation Modal */}
      <Modal
        open={Boolean(deletingProject)}
        onClose={() => !isDeleting && setDeletingProject(null)}
        title="Delete project"
      >
        <div className="flex flex-col gap-4">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-full bg-red-100 text-red-600 shrink-0">
              <AlertTriangle size={20} />
            </div>
            <div className="space-y-1">
              <p className="text-sm font-semibold text-ink">
                Delete "{deletingProject?.name}"?
              </p>
              <p className="text-xs text-ink-muted leading-relaxed">
                Its {deletingProject?.siteCount ?? 0}{" "}
                {deletingProject?.siteCount === 1 ? "site" : "sites"} will also
                be permanently removed. This action cannot be undone.
              </p>
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-2 border-t border-border">
            <Button
              type="button"
              variant="ghost"
              size="sm"
              disabled={isDeleting}
              onClick={() => setDeletingProject(null)}
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant="primary"
              size="sm"
              disabled={isDeleting}
              onClick={handleConfirmDelete}
              className="!bg-red-600 hover:!bg-red-700 !text-white"
            >
              {isDeleting ? "Deleting..." : "Delete project"}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

function EmptyState({ isFiltered, onAdd }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-5 text-center">
      <CanopySVG className="w-32 h-auto text-forest" />
      <div className="flex flex-col gap-1">
        <p className="text-sm font-medium text-ink">
          {isFiltered ? "No projects match this filter." : "No projects yet."}
        </p>
        <p className="text-xs text-ink-muted max-w-xs">
          {isFiltered
            ? 'Try switching to "All" or add a new project.'
            : "Add your first carbon or biodiversity project to get started."}
        </p>
      </div>
      {!isFiltered && (
        <Button variant="secondary" size="sm" onClick={onAdd}>
          <Plus size={13} />
          New project
        </Button>
      )}
    </div>
  );
}
