import { createContext, useContext, useState } from "react";
import { apiFetch } from "../../lib/api";

const AuthContext = createContext(null);
const TOKEN_KEY = "darukaa_token";
const USER_KEY = "darukaa_user";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    () => localStorage.getItem(TOKEN_KEY) || null,
  );
  const [user, setUser] = useState(() => {
    try {
      const raw = localStorage.getItem(USER_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(false);

  function saveAuthData(accessToken, userInfo) {
    setToken(accessToken);
    setUser(userInfo);
    localStorage.setItem(TOKEN_KEY, accessToken);
    localStorage.setItem(USER_KEY, JSON.stringify(userInfo));
  }

  function clearAuthData() {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  async function login({ email, password }) {
    setLoading(true);
    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      const userInfo = { email };
      saveAuthData(data.access_token, userInfo);
      return data;
    } finally {
      setLoading(false);
    }
  }

  async function register({ email, password }) {
    setLoading(true);
    try {
      await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      return await login({ email, password });
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    clearAuthData();
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        loading,
        isAuthenticated: Boolean(token),
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
