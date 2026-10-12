from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator, model_validator

from app.clock import utcnow
from app.constants import DEFAULT_DEADLINE_DAYS


class ProposalStatus(str, Enum):
    active = "active"
    closed = "closed"
    expired = "expired"


class VoteChoice(str, Enum):
    yes = "yes"
    no = "no"
    abstain = "abstain"


def _as_utc_z(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def _blank(value: str) -> str:
    value = " ".join(value.split())
    if not value:
        raise ValueError("must not be blank")
    return value


class ProposalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, examples=["Fund the riverside park lights"])
    description: str = Field(
        min_length=1,
        max_length=5000,
        examples=["Install solar path lights along the riverside walk."],
    )
    deadline: datetime | None = Field(
        default=None,
        description="UTC deadline. Defaults to 2 days from now when omitted.",
        examples=["2030-01-08T18:00:00Z"],
    )

    @field_validator("title", "description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return _blank(value)

    @field_validator("deadline")
    @classmethod
    def normalize_deadline(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value.replace(microsecond=0)

    @model_validator(mode="after")
    def apply_deadline_rules(self):
        now = utcnow()
        if self.deadline is None:
            self.deadline = now + timedelta(days=DEFAULT_DEADLINE_DAYS)
        elif self.deadline <= now:
            raise ValueError("deadline must be in the future")
        return self


class VoteCreate(BaseModel):
    vote: VoteChoice

    @field_validator("vote", mode="before")
    @classmethod
    def normalize_choice(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value


class VoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    proposal_id: int
    voter_name: str
    vote: VoteChoice
    voted_at: datetime

    @field_serializer("voted_at", when_used="json")
    def serialize_voted_at(self, value: datetime) -> str:
        return _as_utc_z(value)


class ProposalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    created_at: datetime
    deadline: datetime
    status: ProposalStatus
    yes_count: int = 0
    no_count: int = 0
    abstain_count: int = 0
    total_votes: int = 0

    @field_serializer("created_at", "deadline", when_used="json")
    def serialize_times(self, value: datetime) -> str:
        return _as_utc_z(value)


class ProposalDetail(ProposalOut):
    votes: list[VoteOut] = Field(default_factory=list)
