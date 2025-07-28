import os
from pathlib import Path
from sqlalchemy import Column, Integer, String, Float, create_engine, select
from sqlalchemy.orm import declarative_base, Session

DB_PATH = Path(__file__).resolve().parent.parent / "landmarks.sqlite3"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Landmark(Base):
    __tablename__ = "landmarks"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    height_m = Column(Float, nullable=False)


def init_db():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if session.query(Landmark).count() == 0:
            session.add_all(
                [
                    Landmark(name="Eiffel Tower", height_m=300.0),
                    Landmark(name="Empire State Building", height_m=381.0),
                    Landmark(name="Burj Khalifa", height_m=828.0),
                ]
            )
            session.commit()


def get_best_analogy(vam_m_per_h: float) -> str:
    with Session(engine) as session:
        landmarks = session.scalars(select(Landmark)).all()
    if not landmarks:
        return "No landmarks available"
    # choose landmark with height closest to vam
    best = min(landmarks, key=lambda lm: abs(vam_m_per_h - lm.height_m))
    ratio = vam_m_per_h / best.height_m
    return f"{ratio:.1f} {best.name}s/hour"

