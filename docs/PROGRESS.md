# Project Progress Log

Rehearsal Studio Booking System  a running record of what's been built, why,
and the exact commands used. Updated at the end of every phase.

Repo: https://github.com/evikody/band-rehearsal-studio-booking

---

## Project summary

A booking website for **one physical band rehearsal room** (not multiple
studios). Customers book without an account (name, email, phone only).
Admin manages bookings, pricing, and studio info through a secured dashboard.

**Operating hours:** MonFri 9:00 AM9:00 PM, SatSun 2:00 PM9:00 PM.

**Booking confirmation rule:** if the booking is for **today**, it's
auto-confirmed. If it's for a **future date**, it's `pending` until an admin
approves or rejects it. (Earlier design discussion floated a rolling
"within 24 hours" window  the finalized rule is simpler and unambiguous:
same calendar day = confirmed, any future day = pending.)

**Booking statuses:** `pending`, `confirmed`, `rejected`, `cancelled`,
`completed`. Only `pending` and `confirmed` block the schedule.

**Tech stack:** React + TypeScript + Vite + Tailwind (frontend, not started
yet)  Python + FastAPI (backend)  PostgreSQL + SQLAlchemy + Alembic
(database)  Docker + Docker Compose (dev/prod)  Nginx + HTTPS (production,
not started yet)  GitHub Actions + Terraform (DevOps, not started yet) 
Prometheus + Grafana + Loki + Grafana Alloy (monitoring, not started yet).
Kubernetes explicitly deferred.

**Working style (as of this point):** Claude writes all code and gives exact
terminal commands one step at a time; user runs commands, tests, and reports
output/errors back.

---

## Phase 0  Project scaffolding

**Goal:** repo structure and initial architecture decision, no app code yet.

**Created:**
```
rehearsal-studio-booking/
 backend/
 frontend/
 docs/adr/0001-initial-architecture.md
 .github/workflows/
 .gitignore
 README.md
 docker-compose.yml (added later, in the Studio API phase)
```

**Key decision (ADR 0001):** three-tier architecture  React SPA  Nginx 
FastAPI  PostgreSQL. FastAPI chosen over Django/Flask for async + typed
validation. PostgreSQL chosen over MySQL specifically for exclusion
constraints (used later to prevent double-booking). Docker Compose (dev)
kept deliberately separate from Terraform (prod infra-as-code).

**Commands used:**
```bash
git init
git add .
git commit -m "Phase 0: initial project scaffolding and architecture decision"
git branch -M main
git remote add origin https://github.com/evikody/band-rehearsal-studio-booking.git
git push -u origin main
```

---

## Phase 1  Domain modeling

**Goal:** define entities and relationships before writing any schema/code.

**Entities decided:**
- `Studio`  kept as a real table (not hardcoded) even though there's only
  ever one row, so a future second room wouldn't require a rewrite.
- `OperatingHours`  weekday/weekend open/close times, editable by admin.
- `Booking`  guest booking, no customer account; stores customer
  name/email/phone directly.
- `Admin`  the only entity with authentication.

**Key decisions confirmed with the user:**
- No customer accounts  guest-style booking only.
- Fixed weekly operating hours (weekday 99, weekend 29).
- Only one studio room  later drove the "singleton resource" API redesign.
- A booking blocks the schedule immediately on creation (pending or
  confirmed), until admin cancels/rejects it.

No commands in this phase  pure design (ER diagram).

---

## System architecture design (pre-code)

Full 11-part architecture reviewed before any implementation: high-level
architecture, frontend architecture, backend architecture (layered:
routers  services  models), database architecture (SQLAlchemy + Alembic +
exclusion constraint), authentication architecture (JWT in httpOnly cookie
for admin only), booking workflow, deployment architecture (single Linux VM
+ Docker Compose + managed Postgres, Kubernetes deferred), CI/CD
(GitHub Actions, manual deploy first), monitoring (structured logs + Sentry
+ hosted uptime check now, Prometheus/Grafana later), backup strategy
(managed snapshots + scheduled `pg_dump`, restore-tested), and security
considerations (HTTPS, bcrypt, rate limiting, CORS allow-list, secrets via
env vars, least-privilege DB user).

No commands in this phase  architecture document only.

---

## Studio API  first backend feature

**Goal:** CRUD endpoints for studio info/pricing.

**Backend structure created:**
```
backend/app/
 main.py
 core/config.py
 db/base.py, session.py
 models/studio.py
 schemas/studio.py
 services/studio_service.py
 api/deps.py, routes/studio.py
backend/alembic/  (env.py, versions/)
backend/requirements.txt, .env.example
docker-compose.yml  (postgres service)
```

**Initial build:** full CRUD (`GET`/`POST`/`PUT`/`DELETE`, list + by-id).

**Correction:** since there is only **one** studio, redesigned as a
**singleton REST resource**  `GET /api/studio` and `PUT /api/studio`, no id
in the URL, no `POST`/`DELETE` (creating a second studio or deleting the
only one aren't real operations). The single row is seeded via a data
migration instead of an admin action.

**Migrations:**
- `0001`  create `studio` table
- `0002`  seed the single studio row
- `0003`  rename table/route from `studios`  `studio` (plural  singular,
  to match the singleton-resource redesign)

**Local dev setup commands:**
```bash
docker compose up -d
cd backend
python -m venv .venv
source .venv/Scripts/activate      # Git Bash on Windows
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

**Once containerized (backend added to docker-compose.yml with its own
Dockerfile):**
```bash
docker compose up -d --build backend        # rebuild after any code change
docker compose exec backend alembic upgrade head   # apply new migrations
docker logs rehearsal-studio-booking-backend-1 --tail 50   # check real errors
```

**Testing commands:**
```bash
curl http://localhost:8000/api/studio
curl -X PUT http://localhost:8000/api/studio \
  -H "Content-Type: application/json" \
  -d '{"name": "Main Rehearsal Room", "description": "...", "price_per_hour": 250}'
curl -i http://localhost:8000/api/studios     # old plural route, should 404
```

**Bugs hit and fixed:**
| Bug | Root cause | Fix |
|---|---|---|
| `curl: Failed to connect` | Nothing had been started yet  setup steps hadn't been run | Walked through Docker  venv  migrate  `uvicorn` in order |
| `relation "studios" does not exist` | Starting containers doesn't auto-run migrations | `docker compose exec backend alembic upgrade head` |
| Edited file didn't reflect new content | Multi-line paste into the MINGW64 console runs each line as a separate shell command instead of pasting as a block | Switched to creating/editing files via `notepad <path>` |
| `notepad ...: cannot find path` | Was in `backend/app`, not the project root, so the relative path didn't resolve | `cd` back to project root before running path-relative commands |
| `git push` rejected | Local and `origin/main` had diverged (a commit existed on GitHub that wasn't local) | `git pull origin main` (merge, handled the auto-opened Vim commit-message screen with `Esc`  `:wq`), then `git push` |

**Git commands (this milestone):**
```bash
git status
git add .
git commit -m "feat: add Studio API as singleton resource with Docker Compose setup"
git push
# rejected  
git pull origin main
# opened Vim for merge commit message  Esc, then :wq, then Enter
git push
```

---

## Role/workflow change

Partway through, the user switched Claude's role from "mentor  user writes
some code" to **primary implementer**: Claude writes all code and gives
exact one-step-at-a-time terminal commands (Git Bash on Windows); user runs
commands, tests, reports output/errors back. `FILE:`/`MODIFY:` format for
code, `DIRECTORY:`/`COMMAND:`/`PURPOSE:`/`EXPECTED:` format for terminal
steps, one logical step at a time, no overloading with many commands at
once.

---

## Booking table + overlap-prevention constraint

**Goal:** the core data-integrity guarantee of the whole system  two
bookings for the same studio can never have overlapping time ranges, even
under simultaneous requests.

**Model:** `backend/app/models/booking.py`  `Booking` with `reference`,
`studio_id` (FK), customer name/email/phone, `start_datetime`/
`end_datetime` (timezone-aware), a **generated column** `time_range`
(Postgres computes this itself from start/end), and a `status` enum
(`pending`/`confirmed`/`rejected`/`cancelled`/`completed`).

**Migration `0004`:**
- Enables the `btree_gist` Postgres extension (lets a GIST index combine an
  equality check on `studio_id` with a range-overlap check on `time_range`
  in one constraint).
- Creates the `booking` table and `booking_status` enum.
- Adds `time_range` as `tstzrange(start_datetime, end_datetime, '[)')` 
  the `'[)'` bound (inclusive start, exclusive end) is what makes
  back-to-back bookings (46pm, 68pm) legal  their ranges touch but don't
  overlap.
- Adds the actual guard:
  ```sql
  ALTER TABLE booking
  ADD CONSTRAINT no_overlapping_active_bookings
  EXCLUDE USING gist (
      studio_id WITH =,
      time_range WITH &&
  )
  WHERE (status IN ('pending', 'confirmed'));
  ```
  Only `pending`/`confirmed` rows are checked  `cancelled`/`rejected`
  bookings free up the slot for real.

**Bugs hit and fixed:**
| Bug | Root cause | Fix |
|---|---|---|
| `type "booking_status" already exists` | Migration explicitly called `booking_status.create(...)` *and* `create_table` auto-creates enum types used by a column  created it twice in one transaction | Removed the explicit `.create()` call; let `create_table` handle it |
| `function tsrange(timestamp with time zone, ...) does not exist` | `tsrange` only works with timezone-naive timestamps; the columns are `timestamp with time zone` on purpose | Used `tstzrange` (both the column type and the function call) instead of `tsrange`, in both the migration and the SQLAlchemy model |

**Verification  direct SQL test in `psql`, bypassing the API entirely:**
```bash
docker compose exec postgres psql -U studio_user -d studio_booking
```
```sql
-- Booking 1: 4-6pm, succeeds
INSERT INTO booking (reference, studio_id, customer_name, customer_email, customer_phone, start_datetime, end_datetime, status)
VALUES ('BK-TEST-1', 1, 'Test A', 'a@test.com', '555-0001', '2026-08-15 16:00:00+00', '2026-08-15 18:00:00+00', 'confirmed');

-- Booking 2: 5-7pm, overlaps booking 1 -- correctly rejected
INSERT INTO booking (...) VALUES ('BK-TEST-2', ..., '2026-08-15 17:00:00+00', '2026-08-15 19:00:00+00', 'confirmed');
-- ERROR: conflicting key value violates exclusion constraint "no_overlapping_active_bookings"

-- Booking 3: 6-8pm, back-to-back with booking 1 -- correctly succeeds
INSERT INTO booking (...) VALUES ('BK-TEST-3', ..., '2026-08-15 18:00:00+00', '2026-08-15 20:00:00+00', 'confirmed');

-- cleanup
DELETE FROM booking WHERE reference LIKE 'BK-TEST-%';
\q
```
**Result: confirmed working exactly as designed**  overlap rejected,
back-to-back allowed.

---

## Current state (as of this entry)

-  Repo scaffolded, ADR 0001 committed
-  Domain model + full architecture designed
-  Studio singleton API working (`GET`/`PUT /api/studio`), containerized,
  migrated, tested, committed, pushed
-  `booking` table + overlap-prevention exclusion constraint created and
  verified directly against Postgres
-  Booking API endpoints (schemas, service logic, routes)  not built yet
-  Same-day auto-confirm / future-date pending logic  not built yet
-  Booking reference number generation  not built yet
-  Admin authentication  not built yet
-  Admin dashboard  not built yet
-  React frontend  not started
-  Dockerized frontend, production deployment, CI/CD, monitoring,
  backups, Terraform  not started

**Next step:** Booking API  Pydantic schemas, service layer (operating
hours check, overlap check, same-day/future confirmation logic, reference
number generation), and the create/list/admin-action endpoints.