# Community Digital Voting System

A full-stack community voting app built for the **Challenge 06: Community Digital Voting System** brief.

Residents can browse public proposals, sign in, cast one vote per ballot, revoke while a proposal is still active, and admins can force-close early. Proposals expire automatically at their deadline.

## Live demo URLs (local)

After setup:

| Service | URL |
| --- | --- |
| Frontend | http://127.0.0.1:3000 |
| API | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |

## Quick start (Windows)

Requirements: **Python 3.11+**, **Node.js 18+**, **Git** (for cloning).

```bat
git clone https://github.com/shankarac/digital-voting-.git
cd digital-voting-
setupdev.bat
runapplication.bat
```

`setupdev.bat` creates the Python virtual environment, installs dependencies, runs Alembic migrations, seeds demo users, and installs frontend packages.

Optional sample ballots (proposals + votes):

```bat
env\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect('voting.db'); c.executescript(open('seed_data.sql',encoding='utf-8').read()); c.commit()"
```

## Demo accounts

Created automatically by `setupdev.bat` (`python -m app.seed_demo`):

| Role | Email | Password | Display name on ballot |
| --- | --- | --- | --- |
| Admin | `admin@community.local` | `admin1234` | Community Admin |
| Voter | `amina@community.local` | `voter1234` | Amina Shah |
| Voter | `leo@community.local` | `voter1234` | Leo Martins |
| Voter | `priya@community.local` | `voter1234` | Priya Nair |
| Voter | `chris@community.local` | `voter1234` | Chris Adeyemi |

Use **Sign in** on the frontend. Demo buttons on the login screen fill these credentials.

## Authentication

- **Register** → `POST /auth/register` → returns JWT + user profile
- **Login** → `POST /auth/login`
- **Current user** → `GET /auth/me` with `Authorization: Bearer <token>`
- **Sign out** → clear token in the browser (frontend)

Protected actions (require sign-in):

- Create proposal
- Cast vote (uses your account **display name** on the public ballot)
- Revoke **your own** vote only

Public (no login):

- List proposals and see vote counts on the dashboard

Sign-in required to open a proposal ballot, vote, or create a proposal.

Admin close:

- Sign in as an admin account, **or**
- Send header `X-Admin-Key: community-admin` (override with `ADMIN_KEY` env var)

## Voting rules

- One vote per signed-in account per proposal (unique on display name).
- Duplicate vote → `409` until you revoke.
- Change vote → revoke, then vote again (only while `active`).
- Missing deadline → **2 days** from creation.
- After deadline → status becomes `expired`; votes and revokes are rejected.
- Admin close → status `closed` and stays closed.

## Tests

```bat
env\Scripts\python.exe -m pip install -r requirements.txt
env\Scripts\python.exe -m pytest
```

## Python SDK (OpenAPI Generator)

With the API running:

```bat
npx --yes @openapitools/openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g python -o voting_sdk --additional-properties=packageName=voting_sdk,projectName=voting-sdk,packageVersion=1.0.0
env\Scripts\python.exe -m pip install -e voting_sdk
env\Scripts\python.exe examples\use_sdk.py
```

A generated copy is already included under `voting_sdk/`.

## Project structure

```text
app/                 FastAPI backend, auth, voting rules
alembic/             SQLite migrations
frontend/            React + Vite UI with login/register
tests/               Backend unit tests
voting_sdk/          Generated Python SDK
seed_data.sql        Optional sample proposals
setupdev.bat         One-shot dev setup
runapplication.bat   Start API + frontend
```

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///./voting.db` | SQLite database file |
| `ADMIN_KEY` | `community-admin` | Shared admin close key |
| `JWT_SECRET` | `change-me-in-production` | JWT signing secret |
| `JWT_EXPIRE_MINUTES` | `10080` (7 days) | Token lifetime |

## Challenge submission

**Repository:** https://github.com/shankarac/digital-voting-

### Setup instructions (Windows)

1. Install **Python 3.11+** and **Node.js 18+**.
2. Clone and enter the repo:
   ```bat
   git clone https://github.com/shankarac/digital-voting-.git
   cd digital-voting-
   ```
3. One-time setup:
   ```bat
   setupdev.bat
   ```
   Creates `env`, installs packages, runs migrations, seeds demo users.
4. Start the app:
   ```bat
   runapplication.bat
   ```
5. Open **http://127.0.0.1:3000** (frontend). API docs: **http://127.0.0.1:8000/docs**
6. Optional sample proposals:
   ```bat
   env\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect('voting.db'); c.executescript(open('seed_data.sql',encoding='utf-8').read()); c.commit()"
   ```
7. Run tests:
   ```bat
   env\Scripts\python.exe -m pytest
   ```

### Demo login

- Voter: `amina@community.local` / `voter1234`
- Admin: `admin@community.local` / `admin1234`

### Deliverables in this repo

| Item | Location |
| --- | --- |
| FastAPI backend | `app/` |
| SQLite + Alembic | `alembic/`, `voting.db` after setup |
| React frontend | `frontend/` |
| OpenAPI Python SDK | `voting_sdk/` |
| Setup scripts | `setupdev.bat`, `runapplication.bat` |
| Backend tests | `tests/` |

## Notes

- Docker is not used (per challenge rules).
- Alembic is invoked as `python -m alembic` because some Windows environments block `alembic.exe` under Device Guard.
- This is a coding-challenge app, not a production election system.
