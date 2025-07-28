import hmac
import hashlib
import os
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from fastapi.responses import JSONResponse

from . import metrics

SECRET = os.getenv("STRAVA_WEBHOOK_SECRET", "")
router = APIRouter()


def verify_signature(signature: str, body: bytes) -> bool:
    digest = hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


@router.post("/webhook")
async def webhook(request: Request):
    signature = request.headers.get("X-Strava-Signature")
    body = await request.body()
    if not signature or not verify_signature(signature, body):
        raise HTTPException(status_code=400, detail="Invalid signature")
    payload = await request.json()
    elevation = payload.get("elevation_data", [])
    times = [datetime.fromisoformat(t) for t in payload.get("time_data", [])]
    total_elev = payload.get("total_elevation", 0.0)
    distance_km = payload.get("distance_km", 0.0)
    vam = metrics.compute_vam(elevation, times)
    hill = metrics.compute_hill_score(total_elev, distance_km)
    score = metrics.compute_trail_score(vam, hill)
    analogy = metrics.generate_analogy(vam)
    return JSONResponse({"vam": vam, "hill_score": hill, "trail_score": score, "analogy": analogy})

