import graphene
from graphql_jwt.decorators import login_required
from utils import mail

from .models import Profile, User
from .types import ProfileType, UserType


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID())
    user_by_username = graphene.Field(UserType, username=graphene.String())
    user_by_email = graphene.Field(UserType, email=graphene.String())
    profiles = graphene.List(ProfileType)
    profile_by_user_id = graphene.Field(ProfileType, user_id=graphene.String())
    profile_by_username = graphene.Field(ProfileType, username=graphene.String())
    profile_by_email = graphene.Field(ProfileType, email=graphene.String())

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


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    user = graphene.Field(UserType)
    ok = graphene.String()

    def mutate(self, info, username, password, email, first_name=None, last_name=None):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
        )

        base_url = info.context.build_absolute_uri("/")
        # Send email verification
        mail.send_verification_email(user, base_url)

        return CreateUserMutation(user=user, ok="User created successfully. Check your email to verify your account.")


class ResendEmailConfirmationMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.String()

    def mutate(self, info, email, password):
        user = User.objects.get(email=email)
        if user.check_password(password):
            base_url = info.context.build_absolute_uri("/")
            # Send email verification
            mail.send_verification_email(user, base_url)
            return ResendEmailConfirmationMutation(ok="Email sent")
        else:
            raise Exception("Invalid password")


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=False)
        password = graphene.String(required=False)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, username=None, password=None, email=None, first_name=None, last_name=None):
        user = info.context.user

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


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        pass

    ok = graphene.String()

    @login_required
    def mutate(self, info):
        user = info.context.user
        user.delete()
        return DeleteUserMutation(ok="User deleted successfully")


class CreateProfileMutation(graphene.Mutation):
    class Arguments:
        bio = graphene.String(required=False)
        location = graphene.String(required=False)
        birth_date = graphene.Date(required=False)

    profile = graphene.Field(ProfileType)
    ok = graphene.String()

    @login_required
    def mutate(self, info, bio=None, location=None, birth_date=None):
        user = info.context.user
        profile = Profile.objects.get(user=user)

        if not profile:
            profile = Profile.objects.create(user=user, bio=bio, location=location, birth_date=birth_date)
            return CreateProfileMutation(profile=profile, ok="Profile created successfully")

        return CreateProfileMutation(profile=profile, ok="Profile already exists")


class UpdateProfileMutation(graphene.Mutation):
    class Arguments:
        bio = graphene.String(required=False)
        location = graphene.String(required=False)
        birth_date = graphene.Date(required=False)

    profile = graphene.Field(ProfileType)
    ok = graphene.String()

    @login_required
    def mutate(self, info, id, bio=None, location=None, birth_date=None):
        user = info.context.user
        profile = Profile.objects.get(user=user)

        if profile:
            if bio:
                profile.bio = bio
            if location:
                profile.location = location
            if birth_date:
                profile.birth_date = birth_date

            profile.save()
            return UpdateProfileMutation(profile=profile, ok="Profile updated successfully")
        return UpdateProfileMutation(ok="Profile not found")


class DeleteProfileMutation(graphene.Mutation):
    class Arguments:
        pass

    ok = graphene.String()

    @login_required
    def mutate(self, info):
        user = info.context.user
        profile = Profile.objects.get(user=user)

        if profile:
            profile.delete()
            return DeleteProfileMutation(ok="Profile deleted successfully")
        return DeleteProfileMutation(ok="Profile not found")


class VerifyUserEmail(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    ok = graphene.String()

    @login_required
    def mutate(self, info, token):
        email = mail.check_verification_token(token)

        user = User.objects.get(email=email)

        if user:
            user.is_active = True
            user.save()
            return VerifyUserEmail(ok="Email verified successfully")
        return VerifyUserEmail(ok="Email verification failed")


# Aggregate mutation class
class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    resend_email_confirmation = ResendEmailConfirmationMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
    verify_user = VerifyUserEmail.Field()
    create_profile = CreateProfileMutation.Field()
    update_profile = UpdateProfileMutation.Field()
    delete_profile = DeleteProfileMutation.Field()
