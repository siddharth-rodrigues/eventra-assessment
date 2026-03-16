import { FormEvent, useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { addGuest, getEvent, listGuests } from "../api";
import type { Event, Guest } from "../types";

export default function EventDetail() {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<Event | null>(null);
  const [guests, setGuests] = useState<Guest[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (id) {
      loadData(id);
    }
  }, [id]);

  async function loadData(eventId: string) {
    try {
      const [ev, g] = await Promise.all([
        getEvent(eventId),
        listGuests(eventId),
      ]);
      setEvent(ev);
      setGuests(g.guests);
    } catch {
      setError("Failed to load event");
    }
  }

  async function handleAddGuest(e: FormEvent) {
    e.preventDefault();
    if (!id) return;
    setError("");
    try {
      await addGuest(id, { name, email });
      setName("");
      setEmail("");
      await loadData(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add guest");
    }
  }

  if (!event) {
    return error ? <p className="error">{error}</p> : <p>Loading...</p>;
  }

  function rsvpStatus(guest: Guest) {
    if (guest.is_attending === true) return "attending";
    if (guest.is_attending === false) return "declined";
    return "pending";
  }

  function rsvpLabel(guest: Guest) {
    if (guest.is_attending === true) return "Attending";
    if (guest.is_attending === false) return "Declined";
    return "Pending";
  }

  return (
    <>
      <Link to="/" className="link" style={{ marginBottom: 16, display: "inline-block" }}>
        &larr; Back to Events
      </Link>

      <div className="card">
        <h2>{event.title}</h2>
        <p style={{ color: "#6b7280", marginBottom: 8 }}>
          {event.event_date}
          {event.location ? ` - ${event.location}` : ""}
        </p>
        <p>{event.description}</p>
        <p style={{ marginTop: 8, fontSize: 13, color: "#9ca3af" }}>
          Status: {event.status} | RSVP:{" "}
          {event.is_rsvp_enabled ? "enabled" : "disabled"}
        </p>
      </div>

      <div className="card">
        <h2>Guests ({guests.length})</h2>

        {error && <p className="error">{error}</p>}

        <form onSubmit={handleAddGuest} className="inline-form" style={{ marginBottom: 16 }}>
          <div className="form-group">
            <input
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button className="btn btn-primary btn-sm">Add</button>
        </form>

        {guests.length === 0 ? (
          <p className="empty" style={{ padding: 20 }}>No guests yet</p>
        ) : (
          guests.map((guest) => (
            <div key={guest.guest_id} className="guest-row">
              <div>
                <span className="name">{guest.name}</span>
                <br />
                <span className="email">{guest.email}</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span className={`status-badge ${rsvpStatus(guest)}`}>
                  {rsvpLabel(guest)}
                </span>
                <Link
                  to={`/rsvp/${guest.guest_id}`}
                  className="btn btn-outline btn-sm"
                  onClick={(e) => e.stopPropagation()}
                >
                  RSVP Link
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </>
  );
}
