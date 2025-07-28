from datetime import datetime
from typing import List

from . import db


def compute_vam(elevation_data: List[float], time_data: List[datetime]) -> float:
    if len(elevation_data) != len(time_data):
        raise ValueError("Elevation and time lists must be the same length")
    if len(elevation_data) < 2:
        return 0.0
    gain = 0.0
    for i in range(1, len(elevation_data)):
        delta = elevation_data[i] - elevation_data[i - 1]
        if delta > 0:
            gain += delta
    total_seconds = (time_data[-1] - time_data[0]).total_seconds()
    if total_seconds == 0:
        return 0.0
    return gain / (total_seconds / 3600.0)


def compute_hill_score(total_elevation: float, distance_km: float) -> float:
    if distance_km == 0:
        return 0.0
    grade = total_elevation / (distance_km * 1000) * 100
    return grade


def compute_trail_score(vam: float, hill_score: float) -> int:
    vam_component = min(vam / 1000, 1.0) * 50
    hill_component = min(hill_score / 10, 1.0) * 50
    score = int(round(vam_component + hill_component))
    return score


def generate_analogy(vam: float) -> str:
    return db.get_best_analogy(vam)

