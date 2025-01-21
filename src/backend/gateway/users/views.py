from django.http import JsonResponse
from django.views import View
from utils import mail
from utils.auth_decorators import view_login_required

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
        print(token)
        email = mail.check_verification_token(token)

        user = User.objects.filter(email=email).first()

        if user:
            user.is_active = True
            user.save()
            return JsonResponse({"message": "Email verified successfully"})
        else:
            return JsonResponse({"message": "Email not verified"}, status=404)
