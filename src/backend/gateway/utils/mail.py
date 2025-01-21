import datetime

import jwt
from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user, base_url):
    token = jwt.encode(
        {"email": user.email, "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)},
        settings.EMAIL_CONF_JWT_SECRET,
        algorithm="HS256",
    )
    subject = "Verify your email"
    message = f"Please click the following link to verify your email: {base_url}/users/verify/?token={token}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def check_verification_token(token):
    try:
        decoded = jwt.decode(token, settings.EMAIL_CONF_JWT_SECRET, algorithms=["HS256"])
        return decoded["email"]
    except jwt.ExpiredSignatureError:
        # Signature has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
