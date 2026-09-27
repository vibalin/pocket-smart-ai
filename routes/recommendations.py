from pathlib import Path
import json

from fastapi import (
    APIRouter,
    Form,
    Request,
    Depends
)

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecommendationHistory
from app.dependencies import get_current_user

from ai.gemini_service import (
    generate_home_recommendation,
    generate_party_recommendation,
    generate_jewelry_recommendation
)


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "app" / "templates")
)


# =========================================================
# HOME INTERIOR
# =========================================================

@router.post("/generate-home")
def generate_home(
    request: Request,
    budget: float = Form(...),
    rooms: str = Form(...),
    style: str = Form(...),
    priorities: str = Form(...),
    location: str = Form(""),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    recommendation = generate_home_recommendation(
        budget=budget,
        rooms=rooms,
        style=style,
        priorities=priorities,
        location=location
    )

    request_data = {
        "rooms": rooms,
        "style": style,
        "priorities": priorities,
        "location": location
    }

    history = RecommendationHistory(
        user_id=current_user.id,
        planner_type="Home Interior",
        budget=budget,
        request_data=json.dumps(request_data),
        recommendation_data=recommendation
    )

    db.add(history)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context={
            "planner": "Home Interior",
            "budget": budget,
            "rooms": rooms,
            "style": style,
            "location": location,
            "recommendation": recommendation
        }
    )


# =========================================================
# PARTY / EVENT
# =========================================================

@router.post("/generate-party")
def generate_party(
    request: Request,
    budget: float = Form(...),
    event_type: str = Form(...),
    guests: int = Form(...),
    location: str = Form(""),
    food_preference: str = Form(""),
    decoration_style: str = Form(""),
    priorities: str = Form(""),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    recommendation = generate_party_recommendation(
        budget=budget,
        event_type=event_type,
        guests=guests,
        location=location,
        food_preference=food_preference,
        decoration_style=decoration_style,
        priorities=priorities
    )

    request_data = {
        "event_type": event_type,
        "guests": guests,
        "location": location,
        "food_preference": food_preference,
        "decoration_style": decoration_style,
        "priorities": priorities
    }

    history = RecommendationHistory(
        user_id=current_user.id,
        planner_type="Party Planner",
        budget=budget,
        request_data=json.dumps(request_data),
        recommendation_data=recommendation
    )

    db.add(history)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="party_recommendation.html",
        context={
            "planner": "Party Planner",
            "budget": budget,
            "event_type": event_type,
            "guests": guests,
            "location": location,
            "food_preference": food_preference,
            "decoration_style": decoration_style,
            "priorities": priorities,
            "recommendation": recommendation
        }
    )


# =========================================================
# JEWELRY
# =========================================================

@router.post("/generate-jewelry")
def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    jewelry_type: str = Form(...),
    metal: str = Form(...),
    style: str = Form(...),
    outfit_description: str = Form(""),
    location: str = Form(""),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    recommendation = generate_jewelry_recommendation(
        budget=budget,
        occasion=occasion,
        jewelry_type=jewelry_type,
        metal=metal,
        style=style,
        outfit_description=outfit_description,
        location=location
    )

    request_data = {
        "occasion": occasion,
        "jewelry_type": jewelry_type,
        "metal": metal,
        "style": style,
        "outfit_description": outfit_description,
        "location": location
    }

    history = RecommendationHistory(
        user_id=current_user.id,
        planner_type="Jewelry Planner",
        budget=budget,
        request_data=json.dumps(request_data),
        recommendation_data=recommendation
    )

    db.add(history)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="jewelry_recommendation.html",
        context={
            "planner": "Jewelry Planner",
            "budget": budget,
            "occasion": occasion,
            "jewelry_type": jewelry_type,
            "metal": metal,
            "style": style,
            "outfit_description": outfit_description,
            "location": location,
            "recommendation": recommendation
        }
    )


# =========================================================
# RECOMMENDATION DETAILS
# =========================================================

@router.get("/recommendations-details/{recommendation_id}")
def recommendation_details(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    history = db.query(
        RecommendationHistory
    ).filter(
        RecommendationHistory.id == recommendation_id,
        RecommendationHistory.user_id == current_user.id
    ).first()

    if not history:
        return {
            "message": "Recommendation not found"
        }

    return {
        "id": history.id,
        "planner_type": history.planner_type,
        "budget": history.budget,
        "request_data": history.request_data,
        "recommendation_data": history.recommendation_data,
        "created_at": history.created_at
    }


# =========================================================
# HISTORY
# =========================================================

@router.get("/history")
def history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    items = db.query(
        RecommendationHistory
    ).filter(
        RecommendationHistory.user_id == current_user.id
    ).order_by(
        RecommendationHistory.created_at.desc()
    ).all()

    return {
        "message": "Recommendation history",
        "items": [
            {
                "id": item.id,
                "planner_type": item.planner_type,
                "budget": item.budget,
                "request_data": item.request_data,
                "recommendation_data": item.recommendation_data,
                "created_at": item.created_at
            }
            for item in items
        ]
    }


# =========================================================
# DELETE HISTORY ITEM
# =========================================================

@router.delete("/history/{recommendation_id}")
def delete_history(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    history_item = db.query(
        RecommendationHistory
    ).filter(
        RecommendationHistory.id == recommendation_id,
        RecommendationHistory.user_id == current_user.id
    ).first()

    if not history_item:
        return {
            "message": "Recommendation not found"
        }

    db.delete(history_item)
    db.commit()

    return {
        "message": "Recommendation deleted successfully"
    }