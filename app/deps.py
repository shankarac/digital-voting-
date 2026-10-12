import hmac
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models import User
from app.security import decode_access_token
from app.services import auth as auth_service

_bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign in required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    return auth_service.get_user_by_id(db, user_id)


def require_admin_access(
    db: Annotated[Session, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    x_admin_key: str | None = Header(default=None, alias="X-Admin-Key"),
) -> None:
    expected = get_settings().admin_key
    if x_admin_key and hmac.compare_digest(x_admin_key, expected):
        return
    if credentials is not None and credentials.scheme.lower() == "bearer":
        try:
            payload = decode_access_token(credentials.credentials)
            user = auth_service.get_user_by_id(db, int(payload["sub"]))
        except (InvalidTokenError, KeyError, TypeError, ValueError, HTTPException):
            user = None
        else:
            if user.role == "admin":
                return
    raise HTTPException(status_code=403, detail="Admin access required.")


DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminAccess = Annotated[None, Depends(require_admin_access)]
