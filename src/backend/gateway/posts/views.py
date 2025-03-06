from django.http import JsonResponse
from django.views import View
from django.db.models import Max
from utils.auth_decorators import view_login_required


from .models import Post, PostMedia


# class based Django view to upload image and video to Post model
class PostImageView(View):
    @view_login_required
    def post(self, request):
        user = request.user
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        order = request.POST.get("order")
        post_id = request.POST.get("post_id")

        if not image and not video:
            return JsonResponse({"message": "Image or video not provided"}, status=400)

        if post_id:
            post = Post.objects.filter(id=post_id, user=user).first()
            if post:
                if order:
                    postMedia = PostMedia.objects.filter(post=post, order=order).first()
                    if postMedia:
                        postMedia.image = image
                        postMedia.video = video
                        postMedia.save()
                    else:
                        PostMedia.objects.create(post=post, image=image, video=video, order=order)
                else:
                    # Create PostMedia with the order equals max order of the post + 1
                    max_order = PostMedia.objects.filter(post=post).aggregate(Max("order"))["order__max"]
                    PostMedia.objects.create(post=post, image=image, video=video, order=max_order + 1)

                return JsonResponse({"message": "Post updated successfully"}, status=200)
            else:
                return JsonResponse({"message": "Post not found"}, status=404)
        else:
            return JsonResponse({"message": "Post ID not provided"}, status=400)
