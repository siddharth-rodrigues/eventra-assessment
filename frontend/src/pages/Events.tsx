import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createEvent, deleteEvent, listEvents } from "../api";
import type { Event } from "../types";

export default function Events() {
  const navigate = useNavigate();
  const [events, setEvents] = useState<Event[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [eventDate, setEventDate] = useState("");
  const [location, setLocation] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    loadEvents();
  }, []);

  async function loadEvents() {
    try {
      const data = await listEvents();
      setEvents(data.events);
    } catch {
      setError("Failed to load events");
    }
  }

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await createEvent({
        title,
        description,
        event_date: eventDate,
        location: location || undefined,
      });
      setTitle("");
      setDescription("");
      setEventDate("");
      setLocation("");
      setShowForm(false);
      await loadEvents();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create event");
    }
  }

  async function handleDelete(eventId: string, e: React.MouseEvent) {
    e.stopPropagation();
    if (!confirm("Delete this event?")) return;
    try {
      await deleteEvent(eventId);
      await loadEvents();
    } catch {
      setError("Failed to delete event");
    }
  }

  return (
    <>
      <div className="page-header">
        <h1>My Events</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Cancel" : "New Event"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {showForm && (
        <div className="card">
          <h2>Create Event</h2>
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Title</label>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                required
              />
            </div>
            <div className="form-group">
              <label>Date</label>
              <input
                type="date"
                value={eventDate}
                onChange={(e) => setEventDate(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Location (optional)</label>
              <input
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>
            <button className="btn btn-primary">Create</button>
          </form>
        </div>
      )}

      {events.length === 0 ? (
        <p className="empty">No events yet. Create your first one!</p>
      ) : (
        events.map((event) => (
          <div
            key={event.event_id}
            className="event-card"
            onClick={() => navigate(`/events/${event.event_id}`)}
          >
            <div>
              <h3>{event.title}</h3>
              <span className="meta">
                {event.event_date}
                {event.location ? ` - ${event.location}` : ""}
              </span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span className="guest-count">
                {event.guest_count} guest{event.guest_count !== 1 ? "s" : ""}
              </span>
              <button
                className="btn btn-danger btn-sm"
                onClick={(e) => handleDelete(event.event_id, e)}
              >
                Delete
              </button>
            </div>
          </div>
        ))
      )}
    </>
  );
}
