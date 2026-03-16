import { Link, Outlet, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getCredits } from "../api";

export default function Layout() {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access_token");
  const [credits, setCredits] = useState<number | null>(null);

  useEffect(() => {
    if (isLoggedIn) {
      getCredits()
        .then((c) => setCredits(c.credits))
        .catch(() => setCredits(null));
    }
  }, [isLoggedIn]);

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <Link to="/">Eventra</Link>
        <div className="nav-right">
          {isLoggedIn ? (
            <>
              {credits !== null && (
                <span className="credits-badge">{credits} credits</span>
              )}
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <Link to="/login">
              <button>Login</button>
            </Link>
          )}
        </div>
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
