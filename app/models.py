from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    planner_type = Column(
        String(50),
        nullable=False
    )

    budget = Column(
        Float,
        nullable=False
    )

    request_data = Column(
        Text,
        nullable=False
    )

    recommendation_data = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )