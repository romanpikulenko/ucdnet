from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("post-image/", csrf_exempt(views.PostImageView.as_view()), name="post-image"),
]
