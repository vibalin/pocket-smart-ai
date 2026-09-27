import json
from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecommendationHistory
from app.dependencies import get_current_user


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "app" / "templates")
)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get("/dashboard")
def dashboard(
    request: Request,
    current_user=Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@router.get("/home-planner")
def home_planner(
    request: Request,
    current_user=Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={}
    )


@router.get("/party-planner")
def party_planner(
    request: Request,
    current_user=Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={}
    )


@router.get("/jewelry-planner")
def jewelry_planner(
    request: Request,
    current_user=Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={}
    )


@router.get("/history-page")
def history_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    items = db.query(
        RecommendationHistory
    ).filter(
        RecommendationHistory.user_id == current_user.id
    ).order_by(
        RecommendationHistory.created_at.desc()
    ).all()

    history_items = []

    for item in items:

        try:
            request_details = json.loads(
                item.request_data
            )
        except Exception:
            request_details = {}

        history_items.append({
            "id": item.id,
            "planner_type": item.planner_type,
            "budget": item.budget,
            "request_details": request_details,
            "recommendation_data": item.recommendation_data,
            "created_at": item.created_at
        })

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "items": history_items
        }
    )


@router.get("/recommendation-page/{recommendation_id}")
def recommendation_page(
    request: Request,
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    item = db.query(
        RecommendationHistory
    ).filter(
        RecommendationHistory.id == recommendation_id,
        RecommendationHistory.user_id == current_user.id
    ).first()

    if not item:
        return RedirectResponse(
            url="/history-page",
            status_code=303
        )

    try:
        request_details = json.loads(
            item.request_data
        )
    except Exception:
        request_details = {}

    context = {
        "planner": item.planner_type,
        "budget": item.budget,
        "recommendation": item.recommendation_data,
        **request_details
    }

    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context=context
    )