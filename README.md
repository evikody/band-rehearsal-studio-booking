# Rehearsal Studio Booking System

A production-quality web application for booking band rehearsal studio time online.
Built incrementally as a learning project covering full-stack development, DevOps,
and cloud infrastructure.

## Status

🚧 **Phase 0 — Project scaffolding.** No application code yet. See `docs/adr/` for
architecture decisions made so far.

## Planned features

**Customers**
- Browse studio, view info and pricing
- View available schedules and book a slot (date, time, duration)
- Receive booking confirmation
- Double-booking is prevented at the database level

**Admins**
- Log in securely
- View, approve, reject, and cancel bookings
- Manage studio room, schedules, and prices
- View booking history

## Tech stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React | Component-based UI, industry-standard |
| Backend | Python + FastAPI | Async, type-validated, auto-generated API docs |
| Database | PostgreSQL | Strong transactional guarantees needed to prevent double-booking |
| Dev environment | Docker + Docker Compose | Reproducible local environment |
| Production | Linux, Nginx, HTTPS | Reverse proxy, TLS termination, static file serving |
| CI/CD | GitHub Actions | Automated testing and (later) deployment |
| Infrastructure | Terraform | Cloud infra as versioned code |
| Later | Kubernetes | Container orchestration at scale |

See `docs/adr/` for the reasoning behind these choices.

## Project structure

```
backend/     FastAPI application
frontend/    React application
docs/adr/    Architecture Decision Records
.github/     CI/CD workflows
```

## Local development

_Instructions will be added once the backend and Docker Compose setup exist (Phase 8)._

## License

TBD.
