from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("pocketsmart_token")

    if not token:
        authorization = request.headers.get(
            "Authorization", ""
        )

        if authorization.startswith("Bearer "):
            token = authorization.replace(
                "Bearer ", "", 1
            )

    if not token:
        if request.url.path.startswith("/api/"):
            raise HTTPException(
                status_code=401,
                detail="Please login first."
            )

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    user_id = decode_access_token(token)

    if not user_id:
        if request.url.path.startswith("/api/"):
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session."
            )

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        if request.url.path.startswith("/api/"):
            raise HTTPException(
                status_code=401,
                detail="User not found."
            )

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return user