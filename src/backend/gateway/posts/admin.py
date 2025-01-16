from django.contrib import admin
from .models import Post, Comment, Follow, Like

# Registering the models to the admin site
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
