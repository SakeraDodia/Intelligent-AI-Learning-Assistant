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

from app.schemas.auth_schema import (
    ForgotPasswordRequest,
    VerifyOtpRequest,
    ResetPasswordRequest
)

from app.utils.otp import (
    generate_otp
)

from app.utils.email import (
    send_otp_email
)

from app.database.db import (
    otp_store
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
    
@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):

    for user in users:

        if user["email"] == data.email:

            user["password"] = hash_password(
                data.new_password
            )

            return {
                "success": True,
                "message": "Password Updated Successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="User Not Found"
    )
@router.post("/send-otp")
def send_otp(data: ForgotPasswordRequest):

    otp = generate_otp()

    otp_store[
        data.email
    ] = otp

    send_otp_email(
        data.email,
        otp
    )

    return {
        "message":
        "OTP Sent Successfully"
    }
    
@router.post("/verify-otp")
def verify_otp(data: VerifyOtpRequest):

    saved_otp = otp_store.get(
        data.email
    )

    if saved_otp != data.otp:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    return {
        "success": True
    }

@router.post(
    "/reset-password"
)
def reset_password(data):

    for user in users:

        if (
            user["email"]
            == data.email
        ):

            user["password"] = (
                hash_password(
                    data.new_password
                )
            )

            otp_store.pop(
                data.email,
                None
            )

            return {
                "message":
                "Password Reset Successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="User Not Found"
    )