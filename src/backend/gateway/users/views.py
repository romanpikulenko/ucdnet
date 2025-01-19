from django.http import JsonResponse
from django.views import View
from .models import Profile
from django.shortcuts import get_object_or_404


# Create your views here.
class ProfileImageView(View):
    def post(self, request, *args, **kwargs):
        profile_id = request.POST["profile_id"]
        profile = get_object_or_404(Profile, id=profile_id)

        avatar = request.FILES.get("avatar")
        if avatar:
            profile.avatar.save(avatar.name, avatar)

        cover_image = request.FILES.get("cover_image")
        if cover_image:
            profile.cover_image.save(cover_image.name, cover_image)

        profile.save()
        return JsonResponse({"status": "success", "message": "Profile images updated successfully."}, status=200)
