from django.db import models
from django.conf import settings


class Post(models.Model):
    def resolve_post_image_path(instance, filename):
        # Define your logic to generate the path for the post image
        return f"posts/{instance.id}/images/{filename}"

    def resolve_post_video_path(instance, filename):
        # Define your logic to generate the path for the post image
        return f"posts/{instance.id}/videos/{filename}"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PostMedia(models.Model):
    def resolve_media_image_path(instance, filename):
        # Define your logic to generate the path for the media image
        return f"posts/{instance.post.id}/images/{filename}"

    def resolve_media_video_path(instance, filename):
        # Define your logic to generate the path for the media image
        return f"posts/{instance.post.id}/videos/{filename}"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media_items")
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=resolve_media_image_path, blank=True, null=True)
    video = models.FileField(upload_to=resolve_media_video_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("post", "order"),)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class LikePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username}"


class LikeComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username}"


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
