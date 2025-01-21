from django.http import JsonResponse
from django.views import View
from utils.auth_decorators import view_login_required

from .models import Profile


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
