from graphene_django import DjangoObjectType

from .models import Profile, User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "profile",
        )


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "location", "birth_date", "created_at", "updated_at", "avatar", "cover_image")
