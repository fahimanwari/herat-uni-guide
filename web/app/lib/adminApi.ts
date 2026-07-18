import { API_BASE } from "./config";
const API = API_BASE;

// Token management
let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(access: string, refresh: string) {
  accessToken = access;
  refreshToken = refresh;
  if (typeof window !== "undefined") {
    localStorage.setItem("admin_access", access);
    localStorage.setItem("admin_refresh", refresh);
  }
}

export function getAccessToken(): string | null {
  if (!accessToken && typeof window !== "undefined") {
    accessToken = localStorage.getItem("admin_access");
    refreshToken = localStorage.getItem("admin_refresh");
  }
  return accessToken;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
  if (typeof window !== "undefined") {
    localStorage.removeItem("admin_access");
    localStorage.removeItem("admin_refresh");
  }
}

// Auto-refresh token
async function refreshAccessToken(): Promise<boolean> {
  if (!refreshToken) return false;
  try {
    const res = await fetch(`${API}/admin/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (res.ok) {
      const data = await res.json();
      setTokens(data.access_token, data.refresh_token);
      return true;
    }
  } catch {}
  clearTokens();
  return false;
}

// Authenticated fetch
async function authFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const token = getAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let res = await fetch(url, { ...options, headers });

  // If 401, try refresh
  if (res.status === 401) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      headers["Authorization"] = `Bearer ${getAccessToken()}`;
      res = await fetch(url, { ...options, headers });
    }
  }

  return res;
}

// API functions
export const adminApi = {
  // Auth
  async login(email: string, password: string) {
    const res = await fetch(`${API}/admin/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error("Login failed");
    const data = await res.json();
    setTokens(data.access_token, data.refresh_token);
    return data;
  },

  // List
  async list(endpoint: string) {
    const res = await authFetch(`${API}${endpoint}`);
    if (!res.ok) throw new Error(`Failed to list: ${res.status}`);
    return res.json();
  },

  // Get
  async get(endpoint: string) {
    const res = await authFetch(`${API}${endpoint}`);
    if (!res.ok) throw new Error(`Failed to get: ${res.status}`);
    return res.json();
  },

  // Create
  async create(endpoint: string, data: any) {
    const res = await authFetch(`${API}${endpoint}`, {
      method: "POST",
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`Failed to create: ${res.status}`);
    return res.json();
  },

  // Update
  async update(endpoint: string, data: any) {
    const res = await authFetch(`${API}${endpoint}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`Failed to update: ${res.status}`);
    return res.json();
  },

  // Delete
  async delete(endpoint: string) {
    const res = await authFetch(`${API}${endpoint}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error(`Failed to delete: ${res.status}`);
    return true;
  },
};
