from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("profile-image/", csrf_exempt(views.ProfileImageView.as_view()), name="profile-image"),
    path("verify/", csrf_exempt(views.VerifyUserEmail.as_view()), name="verify"),
]
