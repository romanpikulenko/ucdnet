from django.contrib import messages
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
            messages.info(request, "Email verified successfully. Your account is activated")
            return redirect("home")

        else:
            messages.error(request, "Email verification failed")
            return redirect("home")


class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        email = mail.check_verification_token(token)

        user = User.objects.filter(email=email).first()

        if user:
            form = ResetPasswordForm()
            return render(request, "users/reset_password.html", {"user": user, "form": form})
        else:
            messages.error(request, "User not found")
            return redirect("home")

    def post(self, request, *args, **kwargs):
        token = request.GET.get("token")
        email = mail.check_verification_token(token)

        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "User not found")
            return redirect("home")

        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            messages.info(request, "Password reset successfully")
            return redirect("home")

        return render(request, "users/reset_password.html", {"user": user, "form": form})
