import { useState } from "react";
import { api } from "../api";
import { errorMessage } from "../format";

function defaultDeadline() {
  const date = new Date(Date.now() + 2 * 24 * 60 * 60 * 1000);
  const pad = (value) => String(value).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

export function ProposalForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [deadline, setDeadline] = useState(defaultDeadline);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    const payload = {
      title: title.trim(),
      description: description.trim(),
    };
    if (!payload.title || !payload.description) {
      setError("Title and description are required.");
      return;
    }
    if (deadline) {
      const parsed = new Date(deadline);
      if (Number.isNaN(parsed.getTime())) {
        setError("Enter a valid deadline.");
        return;
      }
      payload.deadline = parsed.toISOString();
    }
    setSaving(true);
    setError("");
    try {
      const response = await api.post("/proposals/", payload);
      window.location.hash = `#/p/${response.data.id}`;
    } catch (err) {
      setError(errorMessage(err));
      setSaving(false);
    }
  }

  return (
    <section className="panel">
      <h2>New proposal</h2>
      <p className="lede">
        The ballot opens immediately. Leave the deadline as suggested, or clear it and the server uses two days from now.
      </p>
      <form onSubmit={onSubmit} className="stack">
        <label>
          Title
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            maxLength={200}
            required
          />
        </label>
        <label>
          Description
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            maxLength={5000}
            rows={5}
            required
          />
        </label>
        <label>
          Deadline
          <input
            type="datetime-local"
            value={deadline}
            onChange={(event) => setDeadline(event.target.value)}
          />
        </label>
        {error ? <p className="banner" role="alert">{error}</p> : null}
        <div className="actions">
          <button type="submit" disabled={saving}>
            {saving ? "Creating…" : "Open ballot"}
          </button>
          <a className="button secondary" href="#/">
            Cancel
          </a>
        </div>
      </form>
    </section>
  );
}
