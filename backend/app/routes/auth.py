from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.auth_schema import (
    SignupRequest,
    LoginRequest
)

from app.database.db import users

from app.utils.hash import (
    hash_password,
    verify_password
)

from app.utils.jwt import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup")
def signup(data: SignupRequest):

    for user in users:

        if user["email"] == data.email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    users.append({
        "name": data.name,
        "email": data.email,
        "password": hash_password(
            data.password
        )
    })

    return {
        "success": True,
        "message": "Account Created Successfully"
    }


@router.post("/login")
def login(data: LoginRequest):

    for user in users:

        if user["email"] == data.email:

            if verify_password(
                data.password,
                user["password"]
            ):

                token = create_access_token({
                    "email": user["email"]
                })

                return {
                    "success": True,
                    "access_token": token
                }

    raise HTTPException(
        status_code=401,
        detail="Invalid Credentials"
    )