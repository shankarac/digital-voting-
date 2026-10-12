import { useState } from "react";
import { useAuth } from "../auth";
import { errorMessage } from "../format";

const DEMO = [
  { label: "Admin", email: "admin@community.local", password: "admin1234" },
  { label: "Voter", email: "amina@community.local", password: "voter1234" },
];

export function AuthScreen({ mode: initialMode = "login", redirectTo = "#/" }) {
  const { login, register } = useAuth();
  const [mode, setMode] = useState(initialMode);
  const [email, setEmail] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    setPending(true);
    setError("");
    try {
      if (mode === "login") {
        await login(email.trim(), password);
      } else {
        await register(email.trim(), displayName.trim(), password);
      }
      window.location.hash = redirectTo;
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setPending(false);
    }
  }

  function fillDemo(account) {
    setEmail(account.email);
    setPassword(account.password);
    setError("");
  }

  return (
    <section className="auth-shell">
      <div className="auth-card panel">
        <p className="brand">Community ballot</p>
        <h2>{mode === "login" ? "Sign in to vote" : "Create your account"}</h2>
        <p className="lede">
          {mode === "login"
            ? "Use your email and password. Your display name is shown on the public ballot."
            : "Pick a display name voters will see. Passwords must be at least 8 characters."}
        </p>

        <div className="auth-tabs" role="tablist">
          <button
            type="button"
            className={mode === "login" ? "chip on" : "chip"}
            aria-pressed={mode === "login"}
            onClick={() => setMode("login")}
          >
            Sign in
          </button>
          <button
            type="button"
            className={mode === "register" ? "chip on" : "chip"}
            aria-pressed={mode === "register"}
            onClick={() => setMode("register")}
          >
            Register
          </button>
        </div>

        <form className="stack" onSubmit={onSubmit}>
          {mode === "register" ? (
            <label>
              Display name
              <input
                value={displayName}
                onChange={(event) => setDisplayName(event.target.value)}
                placeholder="Amina Shah"
                maxLength={100}
                required
                autoComplete="name"
              />
            </label>
          ) : null}
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@community.local"
              required
              autoComplete="email"
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder={mode === "register" ? "At least 8 characters" : "Your password"}
              minLength={mode === "register" ? 8 : 1}
              required
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
          </label>
          {error ? <p className="banner" role="alert">{error}</p> : null}
          <button type="submit" disabled={pending}>
            {pending ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>

        <div className="demo-box">
          <h3>Demo accounts</h3>
          <p className="muted">Click to fill the form. Run setup once to create these users.</p>
          <div className="demo-actions">
            {DEMO.map((account) => (
              <button
                key={account.email}
                type="button"
                className="secondary"
                onClick={() => fillDemo(account)}
              >
                Use {account.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
