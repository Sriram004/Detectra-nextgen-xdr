from fastapi import Depends, Header, HTTPException
from apps.api.app.schemas.models import User


def get_current_user(authorization: str | None = Header(default=None)) -> User:
    if not authorization:
        return User(username="demo-analyst", role="analyst")

    # Minimal token format for MVP: Bearer username:role
    try:
        token = authorization.replace("Bearer ", "", 1)
        username, role = token.split(":", 1)
        return User(username=username, role=role)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token format") from exc


def require_role(allowed_roles: set[str]):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return checker
