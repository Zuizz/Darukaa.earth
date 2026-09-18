# Darukaa.Earth

A full-stack geospatial dashboard for managing and monitoring carbon and biodiversity conservation projects. An administrator can create projects, draw and register geographic sites on an interactive map, and review time-series analytics — canopy cover, carbon sequestration, biodiversity index, and related metrics — for each site.

Built for the Darukaa.Earth Full-Stack Developer Hackathon Challenge.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Design Decisions & Trade-offs](#design-decisions--trade-offs)
- [Known Limitations](#known-limitations)

---

## Overview

The application serves three core user stories:

- **As an administrator**, I can create a new project and add multiple geographical sites to it.
- **As an administrator**, I can view all projects and sites on an interactive map.
- **As an administrator**, I can click on a specific site to view detailed analytics and performance over time.

The system is built as two independently deployed services — a React frontend and a FastAPI backend — sharing a single PostgreSQL/PostGIS database hosted on Supabase.

---

## Architecture

```
React (Vite)  →  FastAPI (JWT-secured REST API)  →  PostgreSQL + PostGIS (Supabase)
```

- **Frontend** — React, React Router, Tailwind CSS, Mapbox GL JS + Mapbox Draw for polygon geometry, Chart.js for time-series and score visualisations.
- **Backend** — FastAPI, SQLAlchemy + GeoAlchemy2 for spatial ORM mapping, Alembic for migrations, JWT (HS256) for authentication, bcrypt for password hashing.
- **Database** — PostgreSQL with the PostGIS extension enabled on Supabase; site boundaries are stored as `POLYGON` geometry (SRID 4326) with a GIST spatial index for efficient spatial queries.
- **Auth model** — every write endpoint (create/update/delete on projects and sites) is protected by a bearer-token dependency; read endpoints are open to any authenticated session. See [Design Decisions](#design-decisions--trade-offs) for why this is a shared workspace rather than a multi-tenant model.

Frontend and backend are deployed as separate services and communicate entirely over the REST API — the frontend holds no direct database access.

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend framework | React (Vite) |
| Routing | React Router |
| Styling | Tailwind CSS |
| Mapping | Mapbox GL JS + Mapbox GL Draw |
| Charting | Chart.js (react-chartjs-2) |
| Backend framework | FastAPI |
| ORM / spatial | SQLAlchemy + GeoAlchemy2 |
| Migrations | Alembic |
| Auth | JWT (HS256), bcrypt password hashing |
| Database | PostgreSQL + PostGIS (hosted on Supabase) |
| CI/CD | GitHub Actions |
| Pre-commit tooling | Husky, lint-staged, Prettier, Oxlint |
| Deployment | Vercel (frontend and backend deployed as separate projects) |

---

## Database Schema

Four tables cover the full data model:

### `users`
| Column | Type | Notes |
| --- | --- | --- |
| id | varchar | Primary key |
| email | varchar | Unique, indexed |
| hashed_password | varchar | bcrypt hash, never returned by the API |
| created_at | timestamptz | |

### `projects`
| Column | Type | Notes |
| --- | --- | --- |
| id | varchar | Primary key |
| name | varchar | |
| type | varchar | `carbon` \| `biodiversity` |
| status | varchar | `active` \| `monitoring` \| `archived` |
| description | text | |
| created_at | timestamptz | |
| updated_at | timestamptz | |

### `sites`
| Column | Type | Notes |
| --- | --- | --- |
| id | varchar | Primary key |
| project_id | varchar | Foreign key → `projects.id`, cascade delete |
| name | varchar | |
| site_type | varchar | |
| geometry | `Geometry(POLYGON, 4326)` | GIST-indexed, stored/returned as GeoJSON over the API |
| created_at | timestamptz | |

### `site_metrics`
| Column | Type | Notes |
| --- | --- | --- |
| id | varchar | Primary key |
| site_id | varchar | Foreign key → `sites.id` |
| month | varchar | `YYYY-MM` |
| canopy_cover | float8 | Carbon sites |
| carbon_sequestration | float8 | Carbon sites |
| biomass_density | float8 | Carbon sites |
| biodiversity_index | float8 | Biodiversity sites |
| species_count | int | Biodiversity sites |
| disturbance_index | float8 | Biodiversity sites |

Twelve months of data are generated per site using a seasonal trend model (see [Design Decisions](#design-decisions--trade-offs)).

---

## Local Setup

The frontend and backend are separate deployable units within the same repository and are set up independently.

### Prerequisites
- Node.js 18+
- Python 3.11+
- A Supabase project with the PostGIS extension enabled (or any PostgreSQL instance with PostGIS)
- A Mapbox access token

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_URL to your backend URL
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env   # set DATABASE_URL, DATABASE_URL_DIRECT, JWT_SECRET_KEY
alembic upgrade head
uvicorn app.main:app --reload
```

The database is a hosted Supabase Postgres instance with PostGIS enabled — no local database container is required. `DATABASE_URL` (pooled, port 6543) is used at runtime; `DATABASE_URL_DIRECT` (port 5432) is used by Alembic, since the connection pooler is unreliable for schema-changing operations.

---

## Environment Variables

### Frontend (`frontend/.env`)
| Variable | Description |
| --- | --- |
| `VITE_API_URL` | Base URL of the backend API |
| `VITE_MAPBOX_TOKEN` | Mapbox GL JS access token |

### Backend (`backend/.env`)
| Variable | Description |
| --- | --- |
| `DATABASE_URL` | Pooled Supabase connection string, used at runtime |
| `DATABASE_URL_DIRECT` | Direct Supabase connection string, used by Alembic migrations |
| `JWT_SECRET_KEY` | Secret used to sign JWTs |
| `JWT_EXPIRE_MINUTES` | Token expiry window |

None of these are committed to the repository — both `.env.example` files list the required keys with placeholder values.

---

## API Reference

All endpoints are prefixed by the backend's base URL. Interactive documentation is available at `/docs` (Swagger UI) on the running backend.

| Method | Endpoint | Auth required | Description |
| --- | --- | --- | --- |
| GET | `/health` | No | Service health check |
| POST | `/auth/register` | No | Create a new user account |
| POST | `/auth/login` | No | Exchange credentials for a JWT access token |
| GET | `/projects` | No | List all projects |
| POST | `/projects` | Yes | Create a project |
| GET | `/projects/{id}` | No | Get a single project |
| PATCH | `/projects/{id}` | Yes | Update a project |
| DELETE | `/projects/{id}` | Yes | Delete a project (cascades to its sites) |
| GET | `/sites?project_id=` | No | List sites, optionally filtered by project |
| POST | `/sites` | Yes | Create a site from a GeoJSON polygon |
| GET | `/sites/{id}` | No | Get a single site, geometry returned as GeoJSON |
| DELETE | `/sites/{id}` | Yes | Delete a site |
| GET | `/sites/{id}/metrics` | No | Get the 12-month metrics time series for a site |

---

## CI/CD Pipeline

Two layers of automated quality control run on this project.

### Pre-commit hooks (Husky + lint-staged)

Every commit automatically runs, on staged files only:

```
*.{js,jsx}                → oxlint --fix, prettier --write
*.{json,css,md,html}      → prettier --write
```

If linting fails, the commit is blocked until the issues are resolved.

### GitHub Actions

Every push and pull request to `main` triggers a pipeline with three stages, all of which must pass for the workflow to succeed:

```
Push / PR
   │
   ▼
 Lint   → Frontend lint (Oxlint + Prettier check)
   │
   ▼
 Test   → Backend test suite (auth, CRUD, metrics) run against the database
   │
   ▼
 Build  → Production frontend build (Vite) + backend health check
```

Secrets (database credentials, JWT secret) are configured via GitHub Actions repository secrets and are never committed to the workflow file.

---

## Deployment

Frontend and backend are deployed as two separate Vercel projects:

| Service | Notes |
| --- | --- |
| Frontend | Root: `/frontend`, Build: `npm run build`, Output: `dist` |
| Backend | Deployed as a standalone FastAPI service, exposing `/health` and `/docs` |

Environment-specific configuration (database credentials, JWT secret, API base URL) is managed through Vercel's environment variables rather than committed to the repository. The frontend's production build points at the backend's stable production domain, rather than any per-deployment preview URL.

---


