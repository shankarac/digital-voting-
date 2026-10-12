from fastapi import APIRouter, Path, Response, status

from app.deps import CurrentUser, DbSession
from app.services import voting

router = APIRouter(prefix="/votes", tags=["votes"])


@router.delete(
    "/{vote_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="revoke_vote",
    summary="Revoke a vote",
    description="Deletes a vote only while its proposal is still active.",
    responses={
        404: {"description": "Vote not found"},
        409: {"description": "Proposal is closed or expired"},
    },
)
def revoke_vote(
    db: DbSession,
    current_user: CurrentUser,
    vote_id: int = Path(..., ge=1),
) -> Response:
    voting.revoke_vote(db, vote_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
