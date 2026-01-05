from fastapi import Header, HTTPException
from src.auth.security import decode_token


def get_current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing Authorization")

    token = authorization.split(" ", 1)[1]
    try:
        return decode_token(token)
    except ValueError:
        raise HTTPException(401, "Invalid or expired token")
