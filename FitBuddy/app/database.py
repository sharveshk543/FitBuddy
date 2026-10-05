from pathlib import Path

from sqlalchemy import Column, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ---------------------------------------------------------
# USER / PLAN TABLE
# ---------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    username = Column(
        String(100),
        nullable=False,
    )

    age = Column(
        Integer,
        nullable=False,
    )

    weight = Column(
        Float,
        nullable=False,
    )

    goal = Column(
        String(100),
        nullable=False,
    )

    intensity = Column(
        String(50),
        nullable=False,
    )

    workout_plan = Column(
        Text,
        nullable=True,
    )

    updated_plan = Column(
        Text,
        nullable=True,
    )

    nutrition_tip = Column(
        Text,
        nullable=True,
    )


# ---------------------------------------------------------
# CREATE DATABASE TABLES
# ---------------------------------------------------------

def create_tables():
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# SAVE USER
# ---------------------------------------------------------

def save_user(
    user_id: str,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user is None:
            user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
            )

            db.add(user)

        else:
            user.username = username
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity

        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


# ---------------------------------------------------------
# GET USER
# ---------------------------------------------------------

def get_user(user_id: str):
    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    finally:
        db.close()


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------

def get_all_users():
    db = SessionLocal()

    try:
        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )

    finally:
        db.close()


# ---------------------------------------------------------
# SAVE GENERATED PLAN
# ---------------------------------------------------------

def save_plan(
    user_id: str,
    workout_plan: str,
    nutrition_tip: str,
):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user is None:
            return None

        user.workout_plan = workout_plan
        user.nutrition_tip = nutrition_tip

        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


# ---------------------------------------------------------
# UPDATE PLAN
# ---------------------------------------------------------

def update_plan(
    user_id: str,
    updated_plan: str,
    nutrition_tip: str = None,
):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user is None:
            return None

        user.updated_plan = updated_plan

        if nutrition_tip is not None:
            user.nutrition_tip = nutrition_tip

        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


# ---------------------------------------------------------
# GET ORIGINAL PLAN
# ---------------------------------------------------------

def get_original_plan(user_id: str):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user is None:
            return None

        return user.workout_plan

    finally:
        db.close()