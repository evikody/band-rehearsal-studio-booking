# ADR 0001: Initial Architecture and Technology Stack

**Status:** Accepted
**Date:** 2026-08-09

## Context

We are building a booking system for a band rehearsal studio. Customers need to
browse studios and book time slots without double-booking; admins need to manage
studios, schedules, and bookings. The system must be learnable incrementally and
run in production on real infrastructure.

## Decision

We will use a three-tier architecture:

- **Presentation:** React single-page application
- **Application/logic:** Python + FastAPI REST API
- **Data:** PostgreSQL

Local development will be containerized with Docker Compose. Production will run
on Linux with Nginx as a reverse proxy (TLS termination + static file serving) in
front of the FastAPI app. CI will use GitHub Actions. Cloud infrastructure will be
defined with Terraform. Kubernetes is deferred to a later phase.

## Rationale

- **FastAPI** gives us async support, automatic OpenAPI documentation, and
  Pydantic-based request/response validation — request data is validated by type
  hints rather than manual checks.
- **PostgreSQL** provides transactional guarantees and constraint mechanisms
  (unique/exclusion constraints) needed to prevent double-booking correctly under
  concurrent requests, rather than relying on application-level checks alone.
- **Docker Compose vs. Terraform** solve different problems and are deliberately
  kept separate: Compose reproduces the *local dev environment*; Terraform
  declares *cloud infrastructure* as code. Conflating the two is a common source
  of confusion.
- **Nginx in front of FastAPI** avoids exposing the application server directly to
  the internet, handles HTTPS termination, and serves the built React static
  assets efficiently.
- **GitHub Actions** automates test/lint checks on every push (CI), independent
  from deployment (CD), which will be introduced later once there is an actual
  environment to deploy to.

## Consequences

- Backend and frontend are separate deployable units, each with independent
  dependency management.
- Double-booking prevention logic will be designed carefully in a later phase
  (database constraints, not just application code) — this is a deliberate,
  non-trivial design point, not an afterthought.
- Kubernetes is explicitly out of scope until the simpler deployment model
  (Terraform + a single server or managed service) is working end-to-end.

## Alternatives considered

- **Django (with DRF) instead of FastAPI** — more batteries-included, but heavier
  and less naturally async; FastAPI's typed validation was judged a better fit
  and a better teaching tool for API design.
- **MySQL/SQLite instead of PostgreSQL** — simpler to start with, but weaker
  guarantees around the exclusion constraints we'll need for booking overlap
  prevention.
- **Server-rendered templates instead of React** — simpler, but the goal
  explicitly includes learning a modern SPA frontend.
