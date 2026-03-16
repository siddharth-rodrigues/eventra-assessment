# Eventra

Event management platform with a FastAPI backend and React frontend.

## Task

Deploy this application to AWS so it is accessible via a public URL.

The application runs locally with Docker Compose. Your task is to get it running on AWS infrastructure. You may encounter issues along the way -- diagnosing and fixing them is part of the assessment.

### Requirements

- Application running on an EC2 instance (Free Tier eligible)
- PostgreSQL database on RDS (Free Tier eligible)
- Frontend and API both accessible from the public internet
- All pages functional: login, register, events, guests, RSVP
- All API endpoints functional: health, auth, events, guests, credits

### AWS Account

Use your personal AWS Free Tier account. All required services (EC2 t2.micro/t3.micro, RDS db.t3.micro) are Free Tier eligible. Terminate all resources after we confirm your submission to avoid charges.

### Deliverables

1. **Public URL** where the app is running (frontend loads, API health endpoint returns OK)
2. **`SOLUTION.md`** documenting:
   - Infrastructure setup (what you provisioned and why)
   - Issues found and how you resolved them
   - Changes made beyond what was strictly required, and why
   - What you'd do differently in a production environment
3. **All code/config changes** committed to your forked repo

### Time

Expected effort: 4-6 hours. Please complete within **7 days** of receiving this assessment.

### What We Evaluate

- Can you debug and fix infrastructure issues?
- Can you deploy a multi-service application to AWS?
- Do you think about security?
- Can you document your process clearly?
- Do you go beyond the minimum requirements?

### Tech Stack

**Backend:**
- Python 3.12 / FastAPI
- PostgreSQL 16
- Alembic (database migrations)

**Frontend:**
- React 18 / TypeScript
- Vite (build tool)
- React Router

**Infrastructure:**
- Docker / Docker Compose
- Nginx (reverse proxy + static files)

### Architecture

```
Browser --> Nginx (frontend container, port 80)
              |
              |--> /api/*  --> FastAPI (app container, port 8000) --> PostgreSQL (db)
              |--> /*      --> React static files
```

### API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/health` | No | Health check |
| GET | `/api/v1/live` | No | Liveness probe |
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/access-token` | No | Login (get JWT) |
| POST | `/api/v1/auth/refresh-token` | No | Refresh JWT |
| GET | `/api/v1/auth/me` | Yes | Current user info |
| POST | `/api/v1/events` | Yes | Create event |
| GET | `/api/v1/events` | Yes | List my events |
| GET | `/api/v1/events/{id}` | Yes | Event details |
| PUT | `/api/v1/events/{id}` | Yes | Update event |
| DELETE | `/api/v1/events/{id}` | Yes | Delete event |
| POST | `/api/v1/guests/events/{id}/guests` | Yes | Add guest |
| GET | `/api/v1/guests/events/{id}/guests` | Yes | List guests |
| PATCH | `/api/v1/guests/{id}/rsvp` | No | RSVP (public) |
| GET | `/api/v1/credits/me` | Yes | Credit balance |

### Frontend Pages

| Path | Description |
|------|-------------|
| `/login` | Sign in |
| `/register` | Create account |
| `/` | Dashboard - list events, create new |
| `/events/:id` | Event detail - manage guests |
| `/rsvp/:guestId` | Public RSVP page |

### Local Development

See `.env.example` for required environment variables.

```bash
# Copy env file
cp .env.example .env

# Start all services
docker compose up --build

# Frontend: http://localhost (port 80)
# API:      http://localhost:8000
# Health:   http://localhost:8000/api/v1/health
```

## Submission

1. **Fork** this repository to your own GitHub account
2. Make all your changes (bug fixes, config, infrastructure) and commit to your fork
3. Fill out `SOLUTION.md` with your documentation
4. **Add `siddharth-rodrigues` as a collaborator** on your forked repo (Settings > Collaborators)
5. Email **siddharth.rodrigues@airawath.com** with:
   - Link to your forked repo
   - Public URL where the app is running
   - Any notes about your approach
