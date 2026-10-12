import { useState } from "react";
import { api } from "../api";
import { errorMessage, formatWhen } from "../format";
import { usePolled } from "../hooks";
import { Countdown } from "./Countdown";
import { Tally } from "./Tally";

const CHOICES = [
  ["yes", "Yes"],
  ["no", "No"],
  ["abstain", "Abstain"],
];

export function ProposalDetail({ id, user, isAdmin, signedIn }) {
  const { data, error, loading, refresh } = usePolled(`/proposals/${id}`);
  const [actionError, setActionError] = useState("");
  const [pending, setPending] = useState("");
  const [adminKey, setAdminKey] = useState(
    () => sessionStorage.getItem("voting.adminKey") || "",
  );

  const proposal = data && !Array.isArray(data) ? data : null;
  const voterName = user?.display_name || "";
  const mine = proposal?.votes?.find((vote) => vote.voter_name === voterName);
  const open = proposal?.status === "active";

  async function run(label, task) {
    setPending(label);
    setActionError("");
    try {
      await task();
      await refresh();
    } catch (err) {
      setActionError(errorMessage(err));
    } finally {
      setPending("");
    }
  }

  function cast(choice) {
    run(choice, () => api.post(`/proposals/${id}/vote`, { vote: choice }));
  }

  function revoke() {
    if (!mine) return;
    run("revoke", () => api.delete(`/votes/${mine.id}`));
  }

  function closeProposal(event) {
    event.preventDefault();
    const headers = {};
    if (!isAdmin && adminKey) {
      sessionStorage.setItem("voting.adminKey", adminKey);
      headers["X-Admin-Key"] = adminKey;
    }
    run("close", () => api.patch(`/proposals/${id}/close`, undefined, { headers }));
  }

  return (
    <section className="panel">
      <a className="back" href="#/">
        All proposals
      </a>
      {loading && !proposal ? <p className="muted">Loading proposal…</p> : null}
      {error && !proposal ? <p className="banner" role="alert">{error}</p> : null}
      {proposal ? (
        <>
          <div className="card-top">
            <span className={`pill ${proposal.status}`}>{proposal.status}</span>
            <Countdown deadline={proposal.deadline} status={proposal.status} />
          </div>
          <h2>{proposal.title}</h2>
          <p className="description">{proposal.description}</p>
          <p className="meta">
            Opened {formatWhen(proposal.created_at)} · Deadline {formatWhen(proposal.deadline)}
          </p>
          <Tally proposal={proposal} />

          <div className="vote-box">
            <h3>Your ballot</h3>
            {!signedIn ? (
              <>
                <p className="lede">Sign in to cast or change your vote on this proposal.</p>
                <div className="actions">
                  <a className="button" href="#/login">
                    Sign in
                  </a>
                  <a className="button secondary" href="#/register">
                    Register
                  </a>
                </div>
              </>
            ) : (
              <>
                <p className="lede">
                  Signed in as <strong>{user.display_name}</strong>. One vote per account. Revoke to
                  change your choice while the ballot is active.
                </p>
                {mine ? (
                  <p className="yours">
                    You voted <strong>{mine.vote}</strong>.
                  </p>
                ) : null}
                <div className="actions">
                  {CHOICES.map(([value, label]) => (
                    <button
                      key={value}
                      type="button"
                      className={value}
                      disabled={!open || Boolean(mine) || Boolean(pending)}
                      onClick={() => cast(value)}
                    >
                      {pending === value ? "Saving…" : label}
                    </button>
                  ))}
                  <button
                    type="button"
                    className="secondary"
                    disabled={!open || !mine || Boolean(pending)}
                    onClick={revoke}
                  >
                    {pending === "revoke" ? "Revoking…" : "Revoke vote"}
                  </button>
                </div>
                {!open ? (
                  <p className="muted">
                    This proposal is {proposal.status}, so votes cannot be cast or revoked.
                  </p>
                ) : null}
              </>
            )}
            {actionError ? <p className="banner" role="alert">{actionError}</p> : null}
            {error ? <p className="banner" role="alert">{error}</p> : null}
          </div>

          <h3>Votes</h3>
          {proposal.votes.length === 0 ? <p className="muted">No votes yet.</p> : null}
          {proposal.votes.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Voter</th>
                  <th>Choice</th>
                  <th>When</th>
                </tr>
              </thead>
              <tbody>
                {proposal.votes.map((vote) => (
                  <tr key={vote.id} className={vote.id === mine?.id ? "mine" : undefined}>
                    <td>{vote.voter_name}</td>
                    <td className={`choice ${vote.vote}`}>{vote.vote}</td>
                    <td>{formatWhen(vote.voted_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : null}

          {open ? (
            <form className="admin" onSubmit={closeProposal}>
              <h3>Admin close</h3>
              {isAdmin ? (
                <p className="lede">You are signed in as an admin. You can force-close this ballot.</p>
              ) : (
                <>
                  <p className="lede">Force-close with the shared admin key, or sign in as admin.</p>
                  <label>
                    Admin key
                    <input
                      type="password"
                      value={adminKey}
                      onChange={(event) => setAdminKey(event.target.value)}
                      autoComplete="off"
                    />
                  </label>
                </>
              )}
              <button
                type="submit"
                className="secondary"
                disabled={Boolean(pending) || (!isAdmin && !adminKey)}
              >
                {pending === "close" ? "Closing…" : "Close proposal"}
              </button>
            </form>
          ) : null}
        </>
      ) : null}
    </section>
  );
}
