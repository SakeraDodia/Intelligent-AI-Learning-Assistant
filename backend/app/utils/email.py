import smtplib

from email.mime.text import MIMEText

from dotenv import load_dotenv

import os

load_dotenv()

EMAIL_USER = os.getenv(
    "EMAIL_USER"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)

def send_otp_email(
    email,
    otp
):

    message = MIMEText(
        f"Your OTP is: {otp}"
    )

    message["Subject"] = (
        "Password Reset OTP"
    )

    message["From"] = EMAIL_USER

    message["To"] = email

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        EMAIL_USER,
        EMAIL_PASSWORD
    )

    server.send_message(
        message
    )

    server.quit()