import datetime
import uuid
from fastapi import APIRouter
from service.passport_service import PassportService
from contracts import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest) -> LoginResponse:
    now = int(datetime.datetime.now(datetime.UTC).timestamp())
    passport_service = PassportService()
    token = passport_service.issue({
        "iss": "passport",
        "sub": "user",
        "aud": "user",
        "exp": now + (24 * 60 * 60),  # 1 day in seconds
        "iat": now,
        "nbf": now,
        "jti": str(uuid.uuid4())
    })
    response = LoginResponse(
        token=token,
        token_type="bearer"
    )

    return response.model_dump()


@router.post("/logout")
async def logout():
    return {"message": "Logout"}

@router.get("/me")
async def me():
    return {"message": "Me"}

@router.post("/register")
async def register():
    return {"message": "Register"}

@router.post("/reset password")
async def reset_password():
    return {"message": "Reset Password"}
