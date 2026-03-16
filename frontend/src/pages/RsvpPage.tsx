import { useState } from "react";
import { useParams } from "react-router-dom";
import { rsvp } from "../api";

export default function RsvpPage() {
  const { guestId } = useParams<{ guestId: string }>();
  const [submitted, setSubmitted] = useState(false);
  const [attending, setAttending] = useState<boolean | null>(null);
  const [error, setError] = useState("");

  async function handleRsvp(isAttending: boolean) {
    if (!guestId) return;
    setError("");
    try {
      await rsvp(guestId, isAttending);
      setAttending(isAttending);
      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "RSVP failed");
    }
  }

  if (submitted) {
    return (
      <div className="rsvp-page">
        <h1>{attending ? "See you there!" : "Maybe next time!"}</h1>
        <p>Your response has been recorded.</p>
      </div>
    );
  }

  return (
    <div className="rsvp-page">
      <h1>You're Invited!</h1>
      <p>Will you be attending?</p>
      {error && <p className="error">{error}</p>}
      <div className="rsvp-buttons">
        <button className="btn btn-success" onClick={() => handleRsvp(true)}>
          Accept
        </button>
        <button className="btn btn-outline" onClick={() => handleRsvp(false)}>
          Decline
        </button>
      </div>
    </div>
  );
}
