from django.http import JsonResponse
from django.views import View
from utils.auth_decorators import view_login_required

from .models import Post


# class based Django view to upload image and video to Post model
class PostImageView(View):
    @view_login_required
    def post(self, request):
        # get the image and video files from the request
        user = request.user
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        post_id = request.POST.get("post_id")

        if post_id:
            post = Post.objects.filter(id=post_id, user=user).first()
            if post:
                post.image = image
                post.video = video
                post.save()

                return JsonResponse({"message": "Post updated successfully"}, status=200)
            else:
                return JsonResponse({"message": "Post not found"}, status=404)
        else:
            return JsonResponse({"message": "Post ID not provided"}, status=400)
