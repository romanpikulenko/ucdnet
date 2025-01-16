from graphene import Mutation, ObjectType, String, Field, ID, List
from graphene_django import DjangoObjectType
from .models import User, Profile


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
        )


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "location", "birth_date", "created_at", "updated_at", "avatar", "cover_image")


class QueryUser(ObjectType):
    users = List(UserType)
    user_by_id = Field(UserType, id=ID())
    user_by_username = Field(UserType, username=String())
    user_by_email = Field(UserType, email=String())
    profiles = List(ProfileType)
    profile_by_user_id = Field(ProfileType, user_id=String())
    profile_by_username = Field(ProfileType, username=String())
    profile_by_email = Field(ProfileType, email=String())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user_by_id(self, info, id):
        return User.objects.get(id=id)

    def resolve_user_by_username(self, info, username):
        return User.objects.get(username=username)

    def resolve_user_by_email(self, info, email):
        return User.objects.get(email=email)

    def resolve_profiles(self, info):
        return Profile.objects.all()

    def resolve_profile_by_user_id(self, info, user_id):
        return Profile.objects.get(user__id=user_id)

    def resolve_profile_by_username(self, info, username):
        return Profile.objects.get(user__username=username)

    def resolve_profile_by_email(self, info, email):
        return Profile.objects.get(user__email=email)


class CreateUserMutation(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)
        first_name = String(required=False)
        last_name = String(required=False)

    user = Field(UserType)

    def mutate(self, info, username, password, email, first_name=None, last_name=None):
        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name
        )
        return CreateUserMutation(user=user)


class UpdateUserMutation(Mutation):
    class Arguments:
        id = String(required=True)
        username = String(required=False)
        password = String(required=False)
        email = String(required=False)
        first_name = String(required=False)
        last_name = String(required=False)

    user = Field(UserType)

    def mutate(self, info, id, username=None, password=None, email=None, first_name=None, last_name=None):
        user = User.objects.get(id=id)
        if username:
            user.username = username
        if password:
            user.set_password(password)
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        return UpdateUserMutation(user=user)


class DeleteUserMutation(Mutation):
    class Arguments:
        id = String(required=True)

    ok = String()

    def mutate(self, info, id):
        User.objects.get(id=id).delete()
        return DeleteUserMutation(ok="User deleted successfully")


class CreateProfileMutation(Mutation):
    class Arguments:
        user_id = String(required=True)
        bio = String(required=False)
        location = String(required=False)
        birth_date = String(required=False)
        avatar = String(required=False)
        cover_image = String(required=False)

    profile = Field(ProfileType)

    def mutate(self, info, user_id, bio=None, location=None, birth_date=None, avatar=None, cover_image=None):
        user = User.objects.get(id=user_id)
        profile = Profile.objects.create(
            user=user, bio=bio, location=location, birth_date=birth_date, avatar=avatar, cover_image=cover_image
        )
        return CreateProfileMutation(profile=profile)


class UpdateProfileMutation(Mutation):
    class Arguments:
        id = String(required=True)
        bio = String(required=False)
        location = String(required=False)
        birth_date = String(required=False)
        avatar = String(required=False)
        cover_image = String(required=False)

    profile = Field(ProfileType)

    def mutate(self, info, id, bio=None, location=None, birth_date=None, avatar=None, cover_image=None):
        profile = Profile.objects.get(id=id)
        if bio:
            profile.bio = bio
        if location:
            profile.location = location
        if birth_date:
            profile.birth_date = birth_date
        if avatar:
            profile.avatar = avatar
        if cover_image:
            profile.cover_image = cover_image
        profile.save()
        return UpdateProfileMutation(profile=profile)


class DeleteProfileMutation(Mutation):
    class Arguments:
        id = String(required=True)

    ok = String()

    def mutate(self, info, id):
        Profile.objects.get(id=id).delete()
        return DeleteProfileMutation(ok="Profile deleted successfully")


# Aggregate mutation class
class Mutation(ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    create_profile = CreateProfileMutation.Field()
    update_profile = UpdateProfileMutation.Field()
    delete_profile = DeleteProfileMutation.Field()
