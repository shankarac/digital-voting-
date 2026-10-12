import { useEffect, useState } from "react";
import { AuthProvider, useAuth } from "./auth";
import { AuthScreen } from "./components/AuthScreen";
import { ProposalDetail } from "./components/ProposalDetail";
import { ProposalForm } from "./components/ProposalForm";
import { ProposalList } from "./components/ProposalList";

function routeOf(hash) {
  const value = hash || "#/";
  const detail = value.match(/^#\/p\/(\d+)$/);
  if (detail) return { name: "detail", id: detail[1] };
  if (value === "#/new") return { name: "new" };
  if (value === "#/login") return { name: "login" };
  if (value === "#/register") return { name: "register" };
  return { name: "list" };
}

function AppShell() {
  const { user, loading, logout, isAuthenticated, isAdmin } = useAuth();
  const [hash, setHash] = useState(() => window.location.hash || "#/");
  const route = routeOf(hash);

  useEffect(() => {
    const onHash = () => setHash(window.location.hash || "#/");
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  useEffect(() => {
    if (loading) return;
    if (route.name === "new" && !isAuthenticated) {
      window.location.hash = "#/login";
    }
  }, [loading, route.name, isAuthenticated]);

  if (loading) {
    return (
      <main className="layout center">
        <p className="muted">Checking your session…</p>
      </main>
    );
  }

  if (route.name === "login") {
    return <AuthScreen mode="login" redirectTo="#/" />;
  }
  if (route.name === "register") {
    return <AuthScreen mode="register" redirectTo="#/" />;
  }

  return (
    <>
      <header className="top">
        <div className="top-row">
          <div>
            <p className="brand">Community ballot</p>
            <h1>Digital Voting</h1>
          </div>
          <nav>
            <a href="#/" aria-current={route.name === "list" ? "page" : undefined}>
              Proposals
            </a>
            {isAuthenticated ? (
              <a href="#/new" aria-current={route.name === "new" ? "page" : undefined}>
                New proposal
              </a>
            ) : null}
          </nav>
          <div className="account-box">
            {isAuthenticated ? (
              <>
                <div className="account-chip">
                  <span className="account-name">{user.display_name}</span>
                  <span className="account-meta">
                    {user.email}
                    {isAdmin ? " · admin" : ""}
                  </span>
                </div>
                <button type="button" className="secondary" onClick={logout}>
                  Sign out
                </button>
              </>
            ) : (
              <>
                <a className="button secondary" href="#/login">
                  Sign in
                </a>
                <a className="button" href="#/register">
                  Register
                </a>
              </>
            )}
          </div>
        </div>
      </header>
      <main className="layout">
        {!isAuthenticated && route.name === "list" ? (
          <div className="welcome panel">
            <h2>Welcome</h2>
            <p className="lede">
              Browse open ballots without an account. Sign in to cast one vote per proposal, revoke while
              a ballot is still active, or submit a new proposal.
            </p>
            <div className="actions">
              <a className="button" href="#/login">
                Sign in to vote
              </a>
              <a className="button secondary" href="#/register">
                Create account
              </a>
            </div>
          </div>
        ) : null}
        {route.name === "list" ? <ProposalList signedIn={isAuthenticated} /> : null}
        {route.name === "new" && isAuthenticated ? <ProposalForm /> : null}
        {route.name === "detail" ? (
          <ProposalDetail id={route.id} user={user} isAdmin={isAdmin} signedIn={isAuthenticated} />
        ) : null}
      </main>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
}
