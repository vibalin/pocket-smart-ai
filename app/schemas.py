from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    rooms: str
    style: str
    priorities: str
    location: str = ""


class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    event_type: str
    guests: int = Field(gt=0)
    location: str = ""
    food_preference: str = ""
    decoration_style: str = ""
    priorities: str = ""


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str
    jewelry_type: str
    metal: str
    style: str
    outfit_description: str = ""
    location: str = ""


class ProductRecommendation(BaseModel):
    name: str
    category: str
    estimated_price: float
    reason: str
    platform: str
    search_query: str


class RecommendationResponse(BaseModel):
    planner: str
    title: str
    summary: str
    budget: float
    total_estimated_cost: float
    products: list[ProductRecommendation]
    tips: list[str]
    source: str = "gemini"