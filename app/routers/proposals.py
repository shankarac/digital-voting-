from fastapi import APIRouter, Path, status

from app.deps import AdminAccess, CurrentUser, DbSession
from app.schemas import ProposalCreate, ProposalDetail, ProposalOut, VoteCreate, VoteOut
from app.services import voting

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.post(
    "/",
    response_model=ProposalOut,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_proposal",
    summary="Create a proposal",
    description="Creates an active proposal. If deadline is omitted it is set to 2 days from now.",
)
def create_proposal(
    payload: ProposalCreate,
    db: DbSession,
    _: CurrentUser,
) -> ProposalOut:
    return voting.create_proposal(db, payload)


@router.get(
    "/",
    response_model=list[ProposalOut],
    operation_id="list_proposals",
    summary="List proposals",
    description="Returns every proposal, including closed and expired ones, with current vote counts.",
)
def list_proposals(db: DbSession) -> list[ProposalOut]:
    return voting.list_proposals(db)


@router.get(
    "/{proposal_id}",
    response_model=ProposalDetail,
    operation_id="get_proposal",
    summary="Get a proposal",
    description="Returns one proposal, its vote counts, and the individual votes.",
    responses={404: {"description": "Proposal not found"}},
)
def get_proposal(
    db: DbSession,
    proposal_id: int = Path(..., ge=1),
) -> ProposalDetail:
    return voting.get_proposal_detail(db, proposal_id)


@router.post(
    "/{proposal_id}/vote",
    response_model=VoteOut,
    status_code=status.HTTP_201_CREATED,
    operation_id="cast_vote",
    summary="Cast a vote",
    description=(
        "One vote per voter name. A second vote is rejected with 409 until the first vote is revoked. "
        "Voting is rejected once the proposal is closed or expired."
    ),
    responses={
        404: {"description": "Proposal not found"},
        409: {"description": "Duplicate vote, or the proposal is not active"},
    },
)
def cast_vote(
    payload: VoteCreate,
    db: DbSession,
    current_user: CurrentUser,
    proposal_id: int = Path(..., ge=1),
) -> VoteOut:
    return voting.cast_vote(db, proposal_id, payload, current_user)


@router.patch(
    "/{proposal_id}/close",
    response_model=ProposalOut,
    operation_id="close_proposal",
    summary="Close a proposal",
    description="Admin force-close. Requires an admin account or the X-Admin-Key header.",
    responses={
        403: {"description": "Missing or invalid admin key"},
        404: {"description": "Proposal not found"},
        409: {"description": "Proposal is not active"},
    },
)
def close_proposal(
    db: DbSession,
    _: AdminAccess,
    proposal_id: int = Path(..., ge=1),
) -> ProposalOut:
    return voting.close_proposal(db, proposal_id)
