export interface User {
  user_id: string;
  email: string;
}

export interface AuthTokens {
  token_type: string;
  access_token: string;
  expires_at: number;
  refresh_token: string;
  refresh_token_expires_at: number;
}

export interface Event {
  event_id: string;
  title: string;
  description: string;
  event_date: string;
  event_time: string | null;
  location: string | null;
  occasion: string | null;
  status: string;
  guest_limit: number | null;
  is_rsvp_enabled: boolean;
  host_id: string;
  guest_count: number;
}

export interface Guest {
  guest_id: string;
  name: string;
  email: string;
  phone: string | null;
  is_attending: boolean | null;
  rsvp_responded_at: string | null;
  event_id: string;
}

export interface Credits {
  credits: number;
  plan_type: string;
  last_reset_at: string;
}
