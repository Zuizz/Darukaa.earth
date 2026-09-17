import { useState } from "react";
import Modal from "../../components/Modal";
import Button from "../../components/Button";

const fieldClass =
  "w-full rounded-md border border-border bg-cream px-3 py-2 text-sm text-ink " +
  "placeholder:text-ink-muted/50 focus:outline-none focus:ring-2 focus:ring-forest/30 focus:border-forest";

export default function NewProjectModal({ open, onClose, onSubmit }) {
  const [name, setName] = useState("");
  const [type, setType] = useState("carbon");
  const [description, setDescription] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim()) return;
    onSubmit({ name: name.trim(), type, description: description.trim() });
    // Reset form
    setName("");
    setType("carbon");
    setDescription("");
    onClose();
  }

  return (
    <Modal open={open} onClose={onClose} title="New project">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-ink-muted uppercase tracking-wide">
            Project name
          </label>
          <input
            type="text"
            required
            autoFocus
            placeholder="e.g. Western Ghats Corridor Survey"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={fieldClass}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-ink-muted uppercase tracking-wide">
            Type
          </label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className={fieldClass}
          >
            <option value="carbon">Carbon</option>
            <option value="biodiversity">Biodiversity</option>
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-ink-muted uppercase tracking-wide">
            Description{" "}
            <span className="normal-case font-normal">(optional)</span>
          </label>
          <textarea
            rows={3}
            placeholder="Brief context — location, objective, current phase..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className={`${fieldClass} resize-none`}
          />
        </div>

        <div className="flex justify-end gap-2 pt-1">
          <Button type="button" variant="ghost" size="sm" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            size="sm"
            disabled={!name.trim()}
          >
            Create project
          </Button>
        </div>
      </form>
    </Modal>
  );
}
