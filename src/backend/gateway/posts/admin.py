from django.contrib import admin
from .models import Post, Comment, Follow, LikeComment, LikePost, PostMedia

# Registering the models to the admin site
admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(LikeComment)
admin.site.register(LikePost)
