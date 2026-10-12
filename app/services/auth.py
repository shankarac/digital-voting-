from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.schemas_auth import AuthResponse, LoginRequest, RegisterRequest, UserOut
from app.security import create_access_token, hash_password, verify_password


def _user_out(user: User) -> UserOut:
    return UserOut.model_validate(user)


def register_user(db: Session, payload: RegisterRequest) -> AuthResponse:
    user = User(
        email=str(payload.email).lower(),
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
        role="user",
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError as err:
        db.rollback()
        detail = "An account with this email or display name already exists."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail) from err
    token = create_access_token(user_id=user.id, role=user.role)
    return AuthResponse(access_token=token, user=_user_out(user))


def login_user(db: Session, payload: LoginRequest) -> AuthResponse:
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    token = create_access_token(user_id=user.id, role=user.role)
    return AuthResponse(access_token=token, user=_user_out(user))


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session.")
    return user
