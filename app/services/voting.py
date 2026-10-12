"""Voting rules.

- One vote per voter name per proposal (database unique key).
- A second vote is rejected until the first is revoked.
- Votes can be cast or revoked only while the proposal is active.
- Active proposals past their deadline become expired in one indexed update.
- An admin close sets status to closed and is never overwritten by expiry.
"""

from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy import case, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.clock import utcnow
from app.constants import ACTIVE, CLOSED, EXPIRED
from app.models import Proposal, User, Vote
from app.schemas import ProposalCreate, ProposalDetail, ProposalOut, VoteCreate, VoteOut


@dataclass(frozen=True, slots=True)
class Tally:
    yes: int = 0
    no: int = 0
    abstain: int = 0

    @property
    def total(self) -> int:
        return self.yes + self.no + self.abstain


def sync_expirations(db: Session) -> None:
    """Flip due active proposals to expired. One indexed UPDATE."""
    result = db.execute(
        update(Proposal)
        .where(Proposal.status == ACTIVE, Proposal.deadline <= utcnow())
        .values(status=EXPIRED)
        .execution_options(synchronize_session=False)
    )
    if result.rowcount:
        db.commit()
        db.expire_all()


def _proposal_out(proposal: Proposal, tally: Tally) -> ProposalOut:
    return ProposalOut(
        id=proposal.id,
        title=proposal.title,
        description=proposal.description,
        created_at=proposal.created_at,
        deadline=proposal.deadline,
        status=proposal.status,
        yes_count=tally.yes,
        no_count=tally.no,
        abstain_count=tally.abstain,
        total_votes=tally.total,
    )


def _load_tally_map(db: Session) -> dict[int, Tally]:
    yes = func.coalesce(func.sum(case((Vote.vote == "yes", 1), else_=0)), 0)
    no = func.coalesce(func.sum(case((Vote.vote == "no", 1), else_=0)), 0)
    abstain = func.coalesce(func.sum(case((Vote.vote == "abstain", 1), else_=0)), 0)
    rows = db.execute(select(Vote.proposal_id, yes, no, abstain).group_by(Vote.proposal_id)).all()
    return {
        proposal_id: Tally(int(yes_count), int(no_count), int(abstain_count))
        for proposal_id, yes_count, no_count, abstain_count in rows
    }


def _reject_if_inactive(proposal: Proposal, action: str) -> None:
    if proposal.status == ACTIVE:
        return
    if action == "vote":
        detail = f"Voting is not allowed because the proposal is {proposal.status}."
    elif action == "revoke":
        detail = f"This vote cannot be revoked because the proposal is {proposal.status}."
    else:
        detail = f"Only an active proposal can be closed. Current status is {proposal.status}."
    raise HTTPException(status_code=409, detail=detail)


def get_proposal_or_404(db: Session, proposal_id: int) -> Proposal:
    sync_expirations(db)
    proposal = db.get(Proposal, proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal.status == ACTIVE and proposal.deadline <= utcnow():
        proposal.status = EXPIRED
        db.flush()
    return proposal


def create_proposal(db: Session, payload: ProposalCreate) -> ProposalOut:
    deadline = payload.deadline
    if deadline is None:
        raise HTTPException(status_code=422, detail="deadline must be in the future")
    proposal = Proposal(
        title=payload.title,
        description=payload.description,
        deadline=deadline,
        status=ACTIVE,
        created_at=utcnow(),
    )
    db.add(proposal)
    db.flush()
    return _proposal_out(proposal, Tally())


def list_proposals(db: Session) -> list[ProposalOut]:
    sync_expirations(db)
    proposals = db.scalars(
        select(Proposal).order_by(Proposal.created_at.desc(), Proposal.id.desc())
    ).all()
    tallies = _load_tally_map(db)
    return [_proposal_out(proposal, tallies.get(proposal.id, Tally())) for proposal in proposals]


def get_proposal_detail(db: Session, proposal_id: int) -> ProposalDetail:
    proposal = get_proposal_or_404(db, proposal_id)
    votes = db.scalars(
        select(Vote)
        .where(Vote.proposal_id == proposal.id)
        .order_by(Vote.voted_at.desc(), Vote.id.desc())
    ).all()
    tally = Tally(
        yes=sum(vote.vote == "yes" for vote in votes),
        no=sum(vote.vote == "no" for vote in votes),
        abstain=sum(vote.vote == "abstain" for vote in votes),
    )
    return ProposalDetail(
        id=proposal.id,
        title=proposal.title,
        description=proposal.description,
        created_at=proposal.created_at,
        deadline=proposal.deadline,
        status=proposal.status,
        yes_count=tally.yes,
        no_count=tally.no,
        abstain_count=tally.abstain,
        total_votes=tally.total,
        votes=[VoteOut.model_validate(vote) for vote in votes],
    )


def cast_vote(db: Session, proposal_id: int, payload: VoteCreate, voter: User) -> VoteOut:
    proposal = get_proposal_or_404(db, proposal_id)
    _reject_if_inactive(proposal, "vote")
    voter_name = voter.display_name
    existing = db.scalar(
        select(Vote.id).where(
            Vote.proposal_id == proposal.id,
            Vote.voter_name == voter_name,
        )
    )
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "This voter has already voted on this proposal. "
                "Revoke the existing vote while the proposal is active, then vote again."
            ),
        )
    vote = Vote(
        proposal_id=proposal.id,
        voter_name=voter_name,
        vote=payload.vote.value,
        voted_at=utcnow(),
    )
    db.add(vote)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "This voter has already voted on this proposal. "
                "Revoke the existing vote while the proposal is active, then vote again."
            ),
        ) from None
    return VoteOut.model_validate(vote)


def close_proposal(db: Session, proposal_id: int) -> ProposalOut:
    proposal = get_proposal_or_404(db, proposal_id)
    if proposal.status == CLOSED:
        raise HTTPException(status_code=409, detail="Proposal is already closed.")
    _reject_if_inactive(proposal, "close")
    proposal.status = CLOSED
    db.flush()
    votes = db.scalars(select(Vote.vote).where(Vote.proposal_id == proposal.id)).all()
    tally = Tally(
        yes=sum(vote == "yes" for vote in votes),
        no=sum(vote == "no" for vote in votes),
        abstain=sum(vote == "abstain" for vote in votes),
    )
    return _proposal_out(proposal, tally)


def revoke_vote(db: Session, vote_id: int, voter: User) -> None:
    sync_expirations(db)
    vote = db.get(Vote, vote_id)
    if vote is None:
        raise HTTPException(status_code=404, detail="Vote not found")
    if vote.voter_name != voter.display_name:
        raise HTTPException(status_code=403, detail="You can only revoke your own vote.")
    proposal = db.get(Proposal, vote.proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal.status == ACTIVE and proposal.deadline <= utcnow():
        proposal.status = EXPIRED
        db.flush()
    _reject_if_inactive(proposal, "revoke")
    db.delete(vote)
    db.flush()
