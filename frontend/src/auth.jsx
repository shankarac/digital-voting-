import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api, setAuthToken } from "./api";

const TOKEN_KEY = "voting.accessToken";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || "");
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem(TOKEN_KEY)));

  const applySession = useCallback((nextToken, nextUser) => {
    setToken(nextToken || "");
    setUser(nextUser || null);
    setAuthToken(nextToken || "");
    if (nextToken) {
      localStorage.setItem(TOKEN_KEY, nextToken);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  }, []);

  const refreshMe = useCallback(async () => {
    if (!token) {
      setUser(null);
      setLoading(false);
      return null;
    }
    setAuthToken(token);
    try {
      const response = await api.get("/auth/me");
      setUser(response.data);
      return response.data;
    } catch {
      applySession("", null);
      return null;
    } finally {
      setLoading(false);
    }
  }, [applySession, token]);

  useEffect(() => {
    refreshMe();
  }, [refreshMe]);

  const login = useCallback(
    async (email, password) => {
      const response = await api.post("/auth/login", { email, password });
      applySession(response.data.access_token, response.data.user);
      return response.data.user;
    },
    [applySession],
  );

  const register = useCallback(
    async (email, displayName, password) => {
      const response = await api.post("/auth/register", {
        email,
        display_name: displayName,
        password,
      });
      applySession(response.data.access_token, response.data.user);
      return response.data.user;
    },
    [applySession],
  );

  const logout = useCallback(() => {
    applySession("", null);
  }, [applySession]);

  const value = useMemo(
    () => ({
      user,
      token,
      loading,
      isAuthenticated: Boolean(user),
      isAdmin: user?.role === "admin",
      login,
      register,
      logout,
      refreshMe,
    }),
    [user, token, loading, login, register, logout, refreshMe],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
