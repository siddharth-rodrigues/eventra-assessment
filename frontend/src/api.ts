import type { AuthTokens, Credits, Event, Guest, User } from "./types";

const API_BASE = "/api/v1";

function getToken(): string | null {
  return localStorage.getItem("access_token");
}

function authHeaders(): HeadersInit {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...authHeaders(),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    const message =
      body?.detail && typeof body.detail === "string"
        ? body.detail
        : `Request failed (${res.status})`;
    throw new Error(message);
  }

  return res.json() as Promise<T>;
}

export async function register(
  email: string,
  password: string
): Promise<User> {
  return request<User>("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export async function login(
  email: string,
  password: string
): Promise<AuthTokens> {
  const params = new URLSearchParams({ username: email, password });
  return request<AuthTokens>("/auth/access-token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString(),
  });
}

export async function getMe(): Promise<User> {
  return request<User>("/auth/me");
}

export async function getCredits(): Promise<Credits> {
  return request<Credits>("/credits/me");
}

export async function listEvents(): Promise<{ events: Event[]; total: number }> {
  return request("/events");
}

export async function getEvent(id: string): Promise<Event> {
  return request(`/events/${id}`);
}

export async function createEvent(data: {
  title: string;
  description: string;
  event_date: string;
  location?: string;
  occasion?: string;
}): Promise<Event> {
  return request<Event>("/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function updateEvent(
  id: string,
  data: Partial<{
    title: string;
    description: string;
    event_date: string;
    location: string;
    occasion: string;
  }>
): Promise<Event> {
  return request<Event>(`/events/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function deleteEvent(id: string): Promise<void> {
  await fetch(`${API_BASE}/events/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
}

export async function listGuests(
  eventId: string
): Promise<{ guests: Guest[]; total: number }> {
  return request(`/guests/events/${eventId}/guests`);
}

export async function addGuest(
  eventId: string,
  data: { name: string; email: string; phone?: string }
): Promise<Guest> {
  return request<Guest>(`/guests/events/${eventId}/guests`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function rsvp(
  guestId: string,
  isAttending: boolean
): Promise<Guest> {
  return request<Guest>(`/guests/${guestId}/rsvp`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_attending: isAttending }),
  });
}
