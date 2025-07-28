from datetime import datetime, timedelta
from trailmetrics.app import metrics, db


def setup_module(module):
    db.DB_PATH = db.DB_PATH.parent / "test_landmarks.sqlite3"
    db.engine = db.create_engine(f"sqlite:///{db.DB_PATH}") if hasattr(db, 'create_engine') else None
    db.init_db()


def test_compute_vam():
    start = datetime.now()
    times = [start, start + timedelta(minutes=30), start + timedelta(minutes=60)]
    elev = [0, 100, 150]
    vam = metrics.compute_vam(elev, times)
    assert round(vam, 2) == 150.0


def test_compute_hill_score():
    score = metrics.compute_hill_score(500, 10)
    assert round(score, 2) == 5.0


def test_compute_trail_score():
    score = metrics.compute_trail_score(800, 8)
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_generate_analogy():
    result = metrics.generate_analogy(400)
    assert "hour" in result

