from fastapi import APIRouter, status

from app.deps import CurrentUser, DbSession
from app.schemas_auth import AuthResponse, LoginRequest, RegisterRequest, UserOut
from app.services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="register_user",
    summary="Create an account",
)
def register(payload: RegisterRequest, db: DbSession) -> AuthResponse:
    return auth.register_user(db, payload)


@router.post(
    "/login",
    response_model=AuthResponse,
    operation_id="login_user",
    summary="Sign in",
)
def login(payload: LoginRequest, db: DbSession) -> AuthResponse:
    return auth.login_user(db, payload)


@router.get(
    "/me",
    response_model=UserOut,
    operation_id="get_current_user",
    summary="Current signed-in user",
)
def me(current_user: CurrentUser) -> UserOut:
    return UserOut.model_validate(current_user)
