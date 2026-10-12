import { useMemo, useState } from "react";
import { Countdown } from "./Countdown";
import { Tally } from "./Tally";
import { usePolled } from "../hooks";

const FILTERS = [
  ["all", "All"],
  ["active", "Active"],
  ["closed", "Closed"],
  ["expired", "Expired"],
];

export function ProposalList({ signedIn = false }) {
  const { data, error, loading, refreshing, refresh } = usePolled("/proposals/");
  const [filter, setFilter] = useState("all");
  const [query, setQuery] = useState("");
  const proposals = Array.isArray(data) ? data : [];

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return proposals.filter((proposal) => {
      if (filter !== "all" && proposal.status !== filter) return false;
      if (!needle) return true;
      return (
        proposal.title.toLowerCase().includes(needle) ||
        proposal.description.toLowerCase().includes(needle)
      );
    });
  }, [proposals, filter, query]);

  return (
    <section>
      <div className="section-head">
        <div>
          <h2>Proposals</h2>
          <p className="lede">
            Active, closed, and expired ballots. Counts refresh every few seconds.
            {!signedIn ? " Sign in when you are ready to vote." : ""}
          </p>
        </div>
        <button
          type="button"
          className="secondary refresh-btn"
          disabled={refreshing}
          aria-busy={refreshing}
          onClick={() => refresh({ manual: true })}
        >
          {refreshing ? "Refreshing…" : "Refresh"}
        </button>
      </div>

      <div className="toolbar">
        <div className="filters" role="tablist" aria-label="Filter by status">
          {FILTERS.map(([value, label]) => (
            <button
              key={value}
              type="button"
              className={filter === value ? "chip on" : "chip"}
              aria-pressed={filter === value}
              onClick={() => setFilter(value)}
            >
              {label}
            </button>
          ))}
        </div>
        <input
          className="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search title or description"
          aria-label="Search proposals"
        />
      </div>

      {error ? <p className="banner" role="alert">{error}</p> : null}
      {loading && !data ? <p className="muted">Loading proposals…</p> : null}
      {!loading && data && visible.length === 0 ? (
        <p className="empty">No proposals in this view. Create one to open a ballot.</p>
      ) : null}

      <div className="cards">
        {visible.map((proposal) => (
          <a className="card" href={`#/p/${proposal.id}`} key={proposal.id}>
            <div className="card-top">
              <span className={`pill ${proposal.status}`}>{proposal.status}</span>
              <Countdown deadline={proposal.deadline} status={proposal.status} />
            </div>
            <h3>{proposal.title}</h3>
            <p className="excerpt">{proposal.description}</p>
            <Tally proposal={proposal} />
          </a>
        ))}
      </div>
    </section>
  );
}
