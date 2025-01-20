from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Post


# class based Django view to upload image and video to Post model
class PostImageView(View):
    def post(self, request):
        # get the image and video files from the request
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        post_id = request.POST.get("post_id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post:
                post.image = image
                post.video = video
                post.save()

                return JsonResponse({"message": "Post updated successfully"}, status=200)
            else:
                return JsonResponse({"message": "Post not found"}, status=404)
        else:
            return JsonResponse({"message": "Post ID not provided"}, status=400)
