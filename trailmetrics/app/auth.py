import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import httpx

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise RuntimeError("OAuth environment variables not set")

router = APIRouter()
TOKENS = {}

@router.get("/authorize")
async def authorize():
    url = (
        "https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        "&scope=activity:read_all"
    )
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str):
    token_url = "https://www.strava.com/oauth/token"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            token_url,
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
            },
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")
    data = resp.json()
    TOKENS["access_token"] = data.get("access_token")
    TOKENS["refresh_token"] = data.get("refresh_token")
    return {"message": "Authorization successful"}

