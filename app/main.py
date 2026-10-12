from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, proposals, votes

app = FastAPI(
    title="Community Digital Voting System",
    description=(
        "Vote on public proposals. Each voter has one vote per proposal, "
        "revocable only while the proposal is active. Proposals expire at their deadline "
        "or when an admin closes them."
    ),
    version="1.0.0",
    servers=[{"url": "http://127.0.0.1:8000", "description": "Local API"}],
    openapi_tags=[
        {"name": "auth", "description": "Register, sign in, and read the current account."},
        {
            "name": "proposals",
            "description": "Create, list, inspect, vote on, and close proposals.",
        },
        {
            "name": "votes",
            "description": "Revoke a vote while its proposal is still active.",
        },
    ],
)

@app.middleware("http")
async def no_store(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(proposals.router)
app.include_router(votes.router)
