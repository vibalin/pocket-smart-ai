from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter()


@router.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = email.lower().strip()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return RedirectResponse(
            "/register?error=email_exists",
            status_code=303
        )

    user = User(
        name=name.strip(),
        email=email,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="pocketsmart_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return response


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = email.lower().strip()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not verify_password(
        password,
        user.password_hash
    ):
        return RedirectResponse(
            "/login?error=invalid",
            status_code=303
        )

    token = create_access_token(user.id)

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="pocketsmart_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(
        "/login",
        status_code=303
    )

    response.delete_cookie(
        "pocketsmart_token"
    )

    return response