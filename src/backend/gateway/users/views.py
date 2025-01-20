from django.http import JsonResponse
from django.views import View
from graphql_jwt.decorators import login_required

from .models import Profile


# Create your views here.
class ProfileImageView(View):
    def post(self, request, *args, **kwargs):
        profile_id = request.POST.get("profile_id")
        avatar = request.FILES.get("avatar")
        cover_image = request.FILES.get("cover_image")

        if profile_id:
            profile = Profile.objects.filter(id=profile_id).first()
            if profile:
                profile.avatar = avatar
                profile.cover_image = cover_image
                profile.save()
                return JsonResponse({"message": "Profile image updated successfully"})
            else:
                return JsonResponse({"message": "Profile not found"}, status=404)
        else:
            return JsonResponse({"message": "Profile ID is required"}, status=400)
