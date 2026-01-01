from fastapi import APIRouter, Depends, HTTPException, status

from app import config, schemas
from app.security import create_access_token, get_current_user

router = APIRouter()


@router.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest) -> schemas.TokenResponse:
    if payload.username != config.DEMO_USER or payload.password != config.DEMO_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(payload.username)
    return schemas.TokenResponse(access_token=token)


@router.get("/me", response_model=schemas.UserInfo)
def me(user: schemas.UserInfo = Depends(get_current_user)):
    return user
