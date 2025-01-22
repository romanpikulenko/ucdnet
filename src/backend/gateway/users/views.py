from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from utils import mail
from utils.auth_decorators import view_login_required

from .forms import ResetPasswordForm
from .models import Profile, User


# Create your views here.
class ProfileImageView(View):
    @view_login_required
    def post(self, request, *args, **kwargs):
        user = request.user
        avatar = request.FILES.get("avatar")
        cover_image = request.FILES.get("cover_image")

        profile = Profile.objects.filter(user=user).first()
        if profile:
            profile.avatar = avatar
            profile.cover_image = cover_image
            profile.save()
            return JsonResponse({"message": "Profile image updated successfully"})
        else:
            return JsonResponse({"message": "Profile not found"}, status=404)


class VerifyUserEmail(View):
    def get(self, request, *args, **kwargs):
        # Here is has to be request.GET as url parameters are stored in the GET dict
        token = request.GET.get("token")
        email = mail.check_verification_token(token)

        user = User.objects.filter(email=email).first()

        if user:
            user.is_active = True
            user.save()
            # return users/email_verification.html with success message
            return render(
                request,
                "users/user_operation_result.html",
                {"message": "Email verified successfully. Your account is activated", "status": True},
            )

        else:
            return render(
                request, "users/user_operation_result.html", {"message": "Email verification failed", "status": False}
            )


class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        email = mail.check_verification_token(token)

        user = User.objects.filter(email=email).first()

        if user:
            form = ResetPasswordForm()
            return render(request, "users/reset_password.html", {"user": user, "form": form})
        else:
            return render(request, "users/user_operation_result.html", {"message": "User not found", "status": False})

    def post(self, request, *args, **kwargs):
        token = request.GET.get("token")
        email = mail.check_verification_token(token)

        user = User.objects.filter(email=email).first()

        if not user:
            return render(request, "users/user_operation_result.html", {"message": "User not found", "status": False})

        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            return render(
                request,
                "users/user_operation_result.html",
                {"message": "Password reset successfully", "status": True},
            )

        return render(request, "users/reset_password.html", {"user": user, "form": form})
